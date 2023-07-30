import pytz

from core.celery_ import app
from .service import send_email_register, send_email_change_pwd
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from KaifSchool.models import Lesson


@app.task
def send_email_registration(user_email, user_password):
    send_email_register(user_email, user_password)


@app.task
def send_email_change_password(user_email, user_password):
    send_email_change_pwd(user_email, user_password)


@app.task
def send_lesson_reminder():
    ten_min_from_now = timezone.now().replace(second=0, microsecond=0) + timezone.timedelta(minutes=10)
    lessons = Lesson.objects.filter(lesson_date=ten_min_from_now)
    for lesson in lessons:
        tz = pytz.timezone(lesson.student.timezone)
        lesson_date = lesson.lesson_date.astimezone(tz)
        message = f"Ваш урок на kaifschool.ru начнется через 10 минут в {lesson_date.strftime('%H:%M')}! Мы ждем вас!"
        send_mail(
            _("Напоминание о предстоящем уроке"),
            message,
            'kaifschoola@gmail.com',
            [lesson.student.email],
            fail_silently=False,
        )
