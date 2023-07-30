from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import make_aware
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib import messages
from django.utils.translation import gettext as _
from ..models import LessonCount
from accounts.models import Account
from KaifSchool.forms import LessonForm
from KaifSchool.models import Lesson, Theme, STATUS


def all_lessons(request):
    all_Lessons = Lesson.objects.all()
    out = []
    for lesson in all_Lessons:
        if lesson.theme:
            title = lesson.theme.title
        else:
            title = 'No theme added'
        out.append({
            'title': title,
            'id': lesson.pk,
            'start': lesson.lesson_date,
            'end': lesson.lesson_date + lesson.duration,
        })
    return JsonResponse(out, safe=False)


def add_lesson(request):
    start = request.GET.get("start", None)
    title = request.GET.get("title", None)
    aware_datetime = make_aware(datetime.strptime(start, '%Y-%m-%d %H:%M'))
    teacher_pk = int(request.GET.get("teacher", None))
    student_pk = int(request.GET.get("student", None))
    theme_pk = int(request.GET.get("theme", None))
    teacher = get_object_or_404(get_user_model(), pk=teacher_pk)
    student = get_object_or_404(get_user_model(), pk=student_pk)
    theme = get_object_or_404(Theme, pk=theme_pk)
    lesson = Lesson(title=str(title), lesson_date=aware_datetime,
                    teacher=teacher, student=student, theme=theme)
    lesson.save()
    data = {}
    return JsonResponse(data)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    new_start_date = datetime.strptime(start, '%Y-%m-%d %H:%M')
    new_end_date = datetime.strptime(end, '%Y-%m-%d %H:%M')
    new_duration = new_end_date - new_start_date
    new_duration = timedelta(hours=new_duration.seconds // 3600)
    # продолжительность урока минимум по 1 часу можно менять
    title = request.GET.get("title", None)
    id_ = request.GET.get("id", None)
    lesson = Lesson.objects.get(pk=id_)
    lesson.lesson_date = make_aware(new_start_date)
    lesson.title = title
    lesson.duration = new_duration if new_duration.seconds >= 3600 \
        else timedelta(hours=1)  # нельзя выставить урок меньше часа
    lesson.save()
    data = {'title': lesson.title,
            'new_date': lesson.lesson_date}
    return JsonResponse(data, safe=False)


def remove(request):
    id_ = request.GET.get("id", None)
    lesson = Lesson.objects.get(id=id_)
    lesson.delete()
    data = {}
    return JsonResponse(data)


class LessonCreate(CreateView):
    template_name = 'lessons/lesson-add.html'
    model = Lesson
    form_class = LessonForm

    def post(self, request, *args, **kwargs):
        student = self.kwargs.get('pk')
        duration = float(request.POST.get('duration'))
        form = self.form_class(request.POST)
        lesson_count = LessonCount.objects.filter(student=student).first()
        teacher = request.POST.get('teacher')
        if form.is_valid():
            lesson = form.save(commit=False)
            date = lesson.lesson_date
            if duration == 30:
                lesson.duration = timedelta(minutes=30)
            elif duration == 1:
                lesson.duration = timedelta(hours=1)
            elif duration == 1.5:
                lesson.duration = timedelta(hours=1, minutes=30)
            else:
                lesson.duration = timedelta(hours=2)

            if date.minute < 20:
                lesson.lesson_date = date.replace(minute=00)
            elif date.minute < 45:
                lesson.lesson_date = date.replace(minute=30)
            else:
                lesson.lesson_date = date.replace(hour=date.hour + 1, minute=00)

            if lesson_count.balance > 0:
                lesson_count.balance -= 1
                lesson.student_id = student
                lesson.teacher_id = teacher
                messages.success(request, _('Урок добавлен'))
            elif lesson.is_trial is True:
                lesson.student_id = student
                lesson.teacher_id = teacher
                messages.success(request, _('Пробный урок добавлен'))
            elif lesson_count.balance < 1 and lesson.is_trial is False:
                messages.error(request, _('Урок не добавлен, баланс ученика на нуле'))
                return redirect(reverse('lesson_create', kwargs={'pk': student}))

            lesson.teacher.students_list.add(student)
            lesson_count.save()
            lesson.save()
        return redirect('/auth/users/students')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.kwargs.get('pk')
        context['teachers'] = Account.objects.filter(role='Teacher')
        return context


class LessonDetailView(DetailView):
    template_name = 'lessons/lesson-detail.html'
    model = Lesson
    context_object_name = 'lesson'

    def get_template_names(self):
        user = self.request.user
        if user.role == 'Admin':
            return ['lessons/lesson-detail-admin.html']
        else:
            return ['lessons/lesson-detail.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Lesson.objects.get(pk=self.kwargs['pk'])
        context['lesson_form'] = LessonForm(instance=data)
        context['themes'] = Theme.objects.all()
        return context


class LessonUpdate(UpdateView):
    model = Lesson
    template_name = 'lessons/lesson-update.html'
    form_class = LessonForm

    def form_valid(self, form):
        lesson = form.save()
        duration = float(self.request.POST.get('duration'))
        status = self.request.POST.get('status')
        lesson.status = status
        if duration == 30:
            lesson.duration = timedelta(minutes=30)
        elif duration == 1:
            lesson.duration = timedelta(hours=1)
        elif duration == 1.5:
            lesson.duration = timedelta(hours=1, minutes=30)
        else:
            lesson.duration = timedelta(hours=2)
        lesson_balance = lesson.student.lesson_balance.all()
        for lesson_count in lesson_balance:
            if lesson.is_trial is False and lesson_count.balance < 1:
                messages.error(self.request, _('Баланс ученика связанный с этим уроком на нуле, вы не можете '))
                return redirect(reverse('lesson_update', kwargs={'pk': lesson.pk}))

        # получаем объект с новыми данными
        # проверяем данные длительности на минимальные значения
        # и если нужно исправляем.
        date = lesson.lesson_date
        # if lesson.duration < timedelta(seconds=3600):
        #     lesson.duration = timedelta(seconds=3600)
        # else:
        #     lesson.duration = timedelta(hours=lesson.duration.seconds // 3600)
        # Шаг времени урока - 30 минут. Подменяем время начала урока
        # в зависимости от выставленного
        if date.minute < 15:
            lesson.lesson_date = date.replace(minute=00)
        elif date.minute < 45:
            lesson.lesson_date = date.replace(minute=30)
        else:
            date = date.replace(hour=date.hour + 1, minute=00)
            lesson.lesson_date = date
        lesson.save()
        return redirect('lesson', lesson.pk)

    def get_success_url(self):
        return reverse('lesson', kwargs={'pk': self.object.pk})


class LessonUpdateTheme(TemplateView):
    model = Lesson

    def post(self, request, *args, **kwargs):
        theme = Theme.objects.get(pk=request.POST.get('theme_pk'))
        Lesson.objects.filter(
            pk=request.POST.get('lesson_pk')).update(theme=theme)
        return JsonResponse({
            'success': True,
            'theme': theme.title,
            'lesson': request.POST.get('lesson_pk')
        })


class LessonUpdateStatus(TemplateView):
    model = Lesson

    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs.get('pk'))
        if lesson.status == 'Planned':
            lesson.status = 'Ongoing'
            lesson.save()
            return redirect('lesson', lesson.pk)
        elif lesson.status == 'Ongoing':
            lesson.status = 'Completed'
            lesson.hash_lesson = None
            lesson.session_hash = None
            lesson.save()
            return redirect('education')


class LessonDelete(DeleteView):
    model = Lesson

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")


class LessonsEducationView(TemplateView):
    model = Lesson
    template_name = 'lessons/lesson-list-education.html'
    form_class = LessonForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.role == 'Teacher':
            context['lessons'] = self.model.objects\
                .filter(teacher=request.user).order_by('lesson_date')
        elif request.user.role == 'Student':
            context['lessons'] = self.model.objects.\
                filter(student=request.user).order_by('lesson_date')
        elif request.user.role == 'Admin':
            context['lessons'] = self.model.objects.order_by('lesson_date')
        context["statuses"] = list(STATUS)
        return self.render_to_response(context)


def get_meeting_data(request, id):
    response = request.POST.get('webinarHash')
    response2 = request.POST.get('sessionHash')
    lesson = Lesson.objects.get(pk=id)
    lesson.hash_lesson = response
    lesson.session_hash = response2
    lesson.save()
    return JsonResponse({'success': True, 'message': 'Updated'})

