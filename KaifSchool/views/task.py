from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib import messages
from KaifSchool.forms import TaskForm, TaskAnswerFormSet
from KaifSchool.models import Task, TaskAnswer, Exercise


class TaskInline:
    form_class = TaskForm
    model = Task
    template_name = "tasks/task-create-or-update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('task_list', exercise_id=self.object.exercise_id)

    def formset_answers_valid(self, formset):
        answers = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for answer in answers:
            answer.task = self.object
            answer.save()


class TaskCreate(TaskInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(TaskCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['exercise_id'] = self.kwargs['exercise_id']
        return ctx

    def form_valid(self, form):
        exercise_id = self.kwargs['exercise_id']
        form.instance.exercise_id = exercise_id  # Установка exercise_id для задания
        return super().form_valid(form)

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'answers': TaskAnswerFormSet(prefix='answers')
            }
        else:
            return {
                'answers': TaskAnswerFormSet(self.request.POST or None, self.request.FILES or None, prefix='answers')
            }


class TaskUpdate(TaskInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(TaskUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['exercise_id'] = self.kwargs['exercise_id']
        return ctx

    def get_named_formsets(self):
        return {
            'answers': TaskAnswerFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                         prefix='answers')
        }

    def form_valid(self, form):
        exercise_id = self.kwargs['exercise_id']
        form.instance.exercise_id = exercise_id
        return super().form_valid(form)


class TaskList(ListView):
    model = Task
    template_name = 'tasks/task-list.html'
    context_object_name = 'tasks'
    paginate_by = None
    form_class = TaskForm
    ordering = ['id']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        exercise_id = self.kwargs['exercise_id']
        exercise = Exercise.objects.get(id=exercise_id)
        ctx['exercise'] = exercise
        return ctx

    def get_queryset(self):
        exercise_id = self.kwargs['exercise_id']
        return Task.objects.filter(exercise_id=exercise_id)


def delete_answer(request, exercise_id, pk):
    try:
        answer = TaskAnswer.objects.get(id=pk)
    except TaskAnswer.DoesNotExist:
        messages.success(
            request, 'Object Does not exist'
        )
        return redirect('task_update', exercise_id=exercise_id, pk=answer.task.id)

    answer.delete()
    messages.success(
        request, 'Answer deleted successfully'
    )
    return redirect('task_update', exercise_id=exercise_id, pk=answer.task.id)


def delete_task(request, exercise_id, task_id):
    task = get_object_or_404(Task, exercise_id=exercise_id, id=task_id)
    task.delete()
    return redirect('task_list', exercise_id=exercise_id)
