from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import pytz
from accounts.managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

ROLE = (
    ('Admin', _('Админ')),
    ('Teacher', _('Учитель')),
    ('Student', _('Ученик')),
    ('Curator', _('Куратор')),
    ('Supervisor', _('Руководитель')),
    ('Marathon-curator', _('Куратор-марафонов')),
    ('Content-maker', _('Контент-мейкер')),
    ('Technical-support', _('Техподдержка'))
)

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Account(AbstractUser):
    first_name = models.CharField(
        max_length=200,
        verbose_name='Имя',
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name='Фамилия',
        null=True,
        blank=True
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        null=False,
        blank=False,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Почта',
        null=False,
        blank=False,
        unique=True
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        null=True,
        blank=True,
        upload_to='user_pic'
    )
    role = models.CharField(
        max_length=200,
        verbose_name='Роль',
        null=False,
        blank=False,
        choices=ROLE,
    )
    timezone = models.CharField(
        verbose_name='Часовой пояс',
        null=False,
        blank=False,
        choices=TIMEZONES
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        null=True,
        blank=True,
        unique=True,
    )
    bio_text = models.TextField(
        max_length=2000,
        verbose_name='БИО',
        null=True,
        blank=True
    )
    students_list = models.ManyToManyField(
        to='accounts.Account',
        related_name='teacher_students',
        verbose_name='Список студентов',
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    object = UserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.first_name}'


@receiver(post_save, sender=Account)
def create_user_in_lessoncount(sender, instance, created, **kwargs):
    from KaifSchool.models import LessonCount
    if created and instance.role == 'Student':
        LessonCount.objects.create(student=instance, balance=0)
