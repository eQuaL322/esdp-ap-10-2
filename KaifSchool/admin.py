from django.contrib import admin
from .models import Lesson, LessonCount, Theme, Exercise, Task, TaskAnswer, TaskType
from django_json_widget.widgets import JSONEditorWidget
from django.db import models

admin.site.register(Lesson)
admin.site.register(LessonCount)
admin.site.register(Theme)
admin.site.register(Exercise)
admin.site.register(Task)
admin.site.register(TaskType)


@admin.register(TaskAnswer)
class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
