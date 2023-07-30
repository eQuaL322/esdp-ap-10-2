import json
from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DeleteView, DetailView

from KaifSchool.forms import DateRangeForm
from KaifSchool.models import Lesson, LessonCount
from accounts.forms import LoginForm, UserChangeForm, RegisterForm, UserChangePasswordForm, LessonCountForm
from accounts.models import Account, ROLE
from .tasks import send_email_registration, send_email_change_password


class LoginView(TemplateView):
    form = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, _("Некорректные данные"))
            return redirect("index")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.warning(request, _("Пользователь не найден"))
            return redirect("index")
        login(request, user)
        next_ = request.GET.get("next")
        if next_:
            return redirect(next_)
        return redirect("index")


def logout_view(request):
    logout(request)
    return redirect("index")


class ProfileCreateView(CreateView):
    template_name = "profile-create.html"
    form_class = RegisterForm
    success_url = "profile-create"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['password']
            form.save()
            send_email_registration.delay(form.instance.email, pwd)
            messages.success(request, _('Пользователь добавлен! '))
            return redirect(self.success_url)
        context = {"form": form}
        return self.render_to_response(context)


class UserDetailView(DetailView):
    template_name = 'profile-detail.html'
    model = get_user_model()
    context_object_name = 'user_obj'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object.role == 'Student':
            self.planned_lessons = Lesson.objects.filter(student_id=self.object.pk, status='Planned')
            self.completed_lessons = Lesson.objects.filter(student_id=self.object.pk, status='Completed')
            self.canceled_lessons = Lesson.objects.filter(student_id=self.object.pk, status='Canceled')
        elif self.object.role == 'Teacher':
            self.planned_lessons = Lesson.objects.filter(teacher_id=self.object.pk, status='Planned')
            self.completed_lessons = Lesson.objects.filter(teacher_id=self.object.pk, status='Completed')
            self.canceled_lessons = Lesson.objects.filter(teacher_id=self.object.pk, status='Canceled')
        if self.planned_lessons:
            context["planned_lessons_count"] = self.planned_lessons.count
        else:
            context["planned_lessons_count"] = 0
        if self.completed_lessons:
            context["completed_lessons_count"] = self.completed_lessons.count
        else:
            context["completed_lessons_count"] = 0
        if self.canceled_lessons:
            context["canceled_lessons_count"] = self.canceled_lessons.count
        else:
            context["canceled_lessons_count"] = 0
        context["form"] = DateRangeForm
        return self.render_to_response(context)


def get_lessons_count_by_date_range(request, *args, **kwargs):
    object_ = Account.objects.get(pk=kwargs.get('pk'))
    get_start_date = request.POST.get('start_date')
    start_date = datetime.strptime(get_start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    get_end_date = request.POST.get('end_date')
    end_date = datetime.strptime(get_end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    planned_count = 0
    completed_count = 0
    canceled_count = 0

    if object_.role == 'Student':
        planned_count = Lesson.objects.filter(student_id=object_.pk, status='Planned',
                                              lesson_date__range=[start_date, end_date]).count()
        completed_count = Lesson.objects.filter(student_id=object_.pk, status='Completed',
                                                lesson_date__range=[start_date, end_date]).count()
        canceled_count = Lesson.objects.filter(student_id=object_.pk, status='Canceled',
                                               lesson_date__range=[start_date, end_date]).count()
    elif object_.role == 'Teacher':
        planned_count = Lesson.objects.filter(teacher_id=object_.pk, status='Planned',
                                              lesson_date__range=[start_date, end_date]).count()
        completed_count = Lesson.objects.filter(teacher_id=object_.pk, status='Completed',
                                                lesson_date__range=[start_date, end_date]).count()
        canceled_count = Lesson.objects.filter(teacher_id=object_.pk, status='Canceled',
                                               lesson_date__range=[start_date, end_date]).count()
    return JsonResponse(
        {'planned_count': planned_count, 'completed_count': completed_count, 'canceled_count': canceled_count})


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = "profile-update.html"
    context_object_name = "user_obj"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Профайл успешно изменен!"))
        return response

    def get_context_data(self, **kwargs):
        kwargs["password_form"] = UserChangePasswordForm()
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")


class UserChangePasswordView(UpdateView):
    model = get_user_model()
    form_class = UserChangePasswordForm
    template_name = "profile-detail.html"
    context_object_name = "user_obj"

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            pwd = form.cleaned_data['password']
            send_email_change_password.delay(form.instance.email, pwd)
            messages.success(request, _('Пароль успешно изменен!'))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")


class StudentsListView(ListView):
    template_name = "students-list.html"
    model = get_user_model()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["students"] = Account.objects.filter(role='Student')
        context["qs_json"] = json.dumps(list(Account.objects.filter(role='Student').values()), default=str)
        return context


class TeachersListView(ListView):
    template_name = "teachers-list.html"
    model = get_user_model()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["teachers"] = Account.objects.filter(role='Teacher')
        context["qs_json"] = json.dumps(list(Account.objects.filter(role='Teacher').values()), default=str)
        return context


class StaffListView(ListView):
    template_name = "staff-list.html"
    model = get_user_model()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["staff"] = Account.objects.filter(role__in=['Admin',
                                                            'Curator',
                                                            'Supervisor',
                                                            'Marathon-curator',
                                                            'Content-maker',
                                                            'Technical-support']
                                                  )
        context["qs_json"] = json.dumps(list(Account.objects.filter(role__in=['Admin',
                                                                              'Curator',
                                                                              'Supervisor',
                                                                              'Marathon-curator',
                                                                              'Content-maker',
                                                                              'Technical-support'
                                                                              ]).values()), default=str)
        roles = list(ROLE)
        roles.remove(roles[1])
        roles.remove(roles[1])
        context["roles"] = roles
        return context


class DeleteAccountView(DeleteView):
    model = get_user_model()
    context_object_name = "user_obj"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object.delete()
            next_ = request.GET.get('next')
            if next_:
                return redirect(next)
            return redirect('index')
        else:
            return self.form_invalid(form)


class LessonCountView(CreateView):
    model = LessonCount
    form_class = LessonCountForm

    def post(self, request, *args, **kwargs):
        lesson_count = LessonCount.objects.filter(student_id=request.POST.get('pk')).first()
        if lesson_count:
            lesson_count.balance += int(request.POST.get('balance'))
            lesson_count.save()
            return JsonResponse({'success': True, 'balance': lesson_count.balance})
        else:
            LessonCount.objects.create(student_id=request.POST.get('pk'), balance=request.POST.get('balance'))
            return JsonResponse({'success': True, 'balance': request.POST.get('balance')})
