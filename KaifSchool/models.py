import datetime
from datetime import timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

STATUS = (
    ('Planned', _('Запланирован')),
    ('Ongoing', _('Идет')),
    ('Completed', _('Прошёл')),
    ('Canceled', _('Отменён'))
)


class Lesson(models.Model):
    teacher = models.ForeignKey(
        to='accounts.Account',
        on_delete=models.CASCADE,
        related_name='lessons_as_teacher',
        verbose_name='Учитель',
    )
    student = models.ForeignKey(
        to='accounts.Account',
        on_delete=models.CASCADE,
        related_name='lessons_as_student',
        verbose_name='Студент',
    )
    theme = models.ForeignKey(
        to='Theme',
        on_delete=models.CASCADE,
        related_name='lesson_theme',
        verbose_name='Тема',
        null=True,
        blank=True
    )
    is_trial = models.BooleanField(
        default=False,
        verbose_name=_('Пробный урок'),
    )
    status = models.CharField(
        max_length=200,
        verbose_name=_('Статус'),
        null=False,
        blank=False,
        default='Planned',
        choices=STATUS,
    )
    duration = models.DurationField(
        verbose_name='Продолжительность',
        default=timedelta(hours=1),
        null=False,
        blank=False
    )
    lesson_date = models.DateTimeField(
        verbose_name='Дата и время',
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    hash_lesson = models.CharField(
        verbose_name='Hash meeting',
        null=True,
        blank=True,
    )
    session_hash = models.CharField(
        verbose_name='Session hash',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.teacher} - {self.student} - {self.theme}'


@receiver(pre_save, sender=Lesson)
def remove_seconds(sender, instance, *args, **kwargs):
    if instance.pk is None:
        instance.lesson_date = instance.lesson_date.replace(second=0, microsecond=0)


@receiver(pre_save, sender=Lesson)
def convert_date_to_iso_format(sender, instance, *args, **kwargs):
    if hasattr(instance, 'lesson_date'):
        date_field_value = getattr(instance, 'lesson_date')
        if isinstance(date_field_value, timezone.datetime):
            iso_format_date = date_field_value.isoformat()
            setattr(instance, 'lesson_date', iso_format_date)


class LessonCount(models.Model):
    student = models.ForeignKey(
        to='accounts.Account',
        on_delete=models.CASCADE,
        related_name='lesson_balance',
        verbose_name='Ученик',
    )
    balance = models.PositiveSmallIntegerField(
        verbose_name='Оплаченные уроки',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Оплаченные уроки'
        verbose_name_plural = 'Оплаченные уроки'

    def __str__(self):
        return f'{self.student} - {self.balance}'


class Theme(models.Model):
    title = models.CharField(
        verbose_name='Тема урока',
        max_length=300,
        null=False,
        blank=False
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=4000,
        null=False,
        blank=True
    )
    cover = models.ImageField(
        verbose_name='Обложка',
        null=True,
        blank=True,
        upload_to='theme_img'
    )
    theme_creator = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='theme_creator',
        default=1
    )
    exercise = models.ForeignKey(
        to='Exercise',
        on_delete=models.CASCADE,
        related_name='theme_exercise',
        verbose_name='Упражнение',
        null=True,
        blank=True
    )
    homework = models.ForeignKey(
        to='Exercise',
        on_delete=models.CASCADE,
        related_name='theme_homework',
        verbose_name='Домашнее задание',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return f'{self.title}'


class Exercise(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=250,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'

    def __str__(self):
        return f'{self.title}'


class Task(models.Model):
    question = models.CharField(
        verbose_name='Вопрос',
        max_length=600,
        null=False,
        blank=False
    )
    exercise = models.ForeignKey(
        to='Exercise',
        on_delete=models.CASCADE,
        related_name='task_exercise',
        verbose_name='Упражнение'
    )
    task_type = models.ForeignKey(
        to='TaskType',
        on_delete=models.CASCADE,
        related_name='task_type',
        verbose_name='Тип задания',
    )
    task_body = models.JSONField(
        null=True,
        blank=True
    )
    task_text = models.TextField(
        max_length=2000,
        verbose_name='Текст',
        null=True,
        blank=True
    )
    file = models.FileField(
        verbose_name='Загрузить файл',
        max_length=400,
        upload_to='task_files',
        null=True,
        blank=True
    )
    url = models.CharField(
        verbose_name='Ссылка на ресурс',
        max_length=600,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.question}'


class TaskAnswer(models.Model):
    task = models.ForeignKey(
        to='Task',
        on_delete=models.CASCADE,
        related_name='task_answers',
        verbose_name='Задача'
    )
    answer_text = models.CharField(
        verbose_name='Текст варианта ответа',
        max_length=600,
        null=True,
        blank=True
    )
    is_correct = models.BooleanField(
        verbose_name='Правильный ответ',
        default=False,
    )

    def __str__(self):
        return self.task.question


class TaskType(models.Model):
    title = models.CharField(
        verbose_name='Название типа',
        max_length=600,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = 'Тип задания'
        verbose_name_plural = 'Типы заданий'

    def __str__(self):
        return f'{self.title}'
