from django import forms
from django.contrib.admin import widgets
from django.forms import inlineformset_factory, DateInput

from .models import Exercise
from .models import Lesson, TaskType
from .models import Theme, Task, TaskAnswer


class LessonForm(forms.ModelForm):
    lesson_date = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())

    class Meta:
        model = Lesson
        exclude = ['created_at']
        fields = ('lesson_date', 'is_trial')


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ('title', 'cover', 'description')


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.label = ""


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('title',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['question', 'task_type', 'file', 'url', 'task_text']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'task_type': forms.Select(attrs={'class': 'form-control'}),
            'task_text': forms.Textarea(attrs={'class': 'form-control', 'rows': '10',
                                               'placeholder': 'Напишите здесь текст. Слова и фразы, которые нужно '
                                                              'вставить из рамочки, заключите в квадратные скобки.'
                                                              '                               Пример: '
                                                              'I like [walking] in the park in the morning.'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter URL here'}),
        }


class TaskTestForm(forms.ModelForm):
    class Meta:
        model = TaskAnswer
        fields = '__all__'
        widgets = {
            'answer_text': forms.TextInput(attrs={'class': 'answer-input form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'answer-checkbox'}),
        }


TaskAnswerFormSet = inlineformset_factory(Task, TaskAnswer, form=TaskTestForm, extra=1, can_delete=True,
                                          can_delete_extra=True)


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ['title']
