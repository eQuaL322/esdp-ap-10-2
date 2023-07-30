from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from KaifSchool.forms import ThemeForm, ExerciseForm, LessonForm
from KaifSchool.models import Theme, Exercise, Lesson


class ThemeCatalog(ListView):
    template_name = 'themes/theme-catalog-list.html'
    model = Theme
    ordering = '-id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['themes'] = Theme.objects.all()
        return context


class ThemePersonal(ListView):
    template_name = 'themes/theme-personal-list.html'
    model = Theme
    ordering = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = ThemeForm()
        return context


class ThemeCreate(CreateView):
    template_name = ''
    model = Theme
    form_class = ThemeForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, request.FILES or None)
        if form.is_valid():
            theme = form.save(commit=False)
            theme.theme_creator = self.request.user
            form.save()
            return redirect('theme_list_personal')


class ThemeUpdate(UpdateView):
    template_name = ''
    model = Theme
    context_object_name = 'theme'
    form_class = ThemeForm

    def get_success_url(self):
        return reverse('theme_detail', kwargs={'pk': self.kwargs['pk']})


class ThemeDetail(DetailView):
    template_name = 'themes/theme-detail.html'
    model = Theme
    context_object_name = 'theme'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.exercise is not None:
            self.exercise = Exercise.objects.filter(pk=self.object.exercise.pk).first()
            self.exercise_id = self.exercise.id
        if self.object.homework is not None:
            self.homework = Exercise.objects.filter(pk=self.object.homework.pk).first()
            self.homework_id = self.homework.id
        self.lessons = Lesson.objects.filter(teacher=request.user, status="Planned").order_by('lesson_date')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["exercise_form"] = ExerciseForm()
        data = Theme.objects.get(pk=self.kwargs['pk'])
        context['form'] = ThemeForm(instance=data)
        context['lesson_from'] = LessonForm()
        context['lessons'] = self.lessons
        if self.object.exercise is not None:
            context["exercise_update_form"] = ExerciseForm(instance=self.exercise)
            context["exercise_id"] = self.exercise_id
        if self.object.homework is not None:
            context["homework_update_form"] = ExerciseForm(instance=self.homework)
            context["homework_id"] = self.homework_id
        return context


class ThemeDelete(DeleteView):
    model = Theme

    def get_success_url(self):
        return reverse('theme_list_personal')
