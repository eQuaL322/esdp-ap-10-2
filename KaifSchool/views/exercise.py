from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, UpdateView

from KaifSchool.forms import ExerciseForm
from KaifSchool.models import Exercise, Theme


class ExerciseCreate(CreateView):
    model = Exercise
    form_class = ExerciseForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.save()
            if request.GET['exercise'] == 'exercise':
                Theme.objects.filter(pk=kwargs.get('pk'))\
                    .update(exercise=exercise.pk)
            else:
                Theme.objects.filter(pk=kwargs.get('pk'))\
                    .update(homework=exercise.pk)
            return redirect("task_list", exercise_id=exercise.pk)


class ExerciseDelete(DeleteView):
    model = Exercise

    def post(self, request, *args, **kwargs):
        if request.GET['exercise'] == 'exercise':
            Theme.objects.filter(pk=kwargs.get('theme_pk')).update(exercise="")
            return self.delete(request, *args, **kwargs)
        else:
            Theme.objects.filter(pk=kwargs.get('theme_pk')).update(homework="")
            return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")


class ExerciseUpdate(UpdateView):
    model = Exercise
    context_object_name = 'exercise'
    form_class = ExerciseForm

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")
