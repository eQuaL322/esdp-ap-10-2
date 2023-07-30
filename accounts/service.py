from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


def send_email_register(user_email, user_password):
    send_mail(
        _('Регистрация на сайте kaifschool.ru'),
        _('Вы зарегистрированы на сайте kaifschool.ru! Ваш пароль для входа:') + user_password,
        'kaifschoola@gmail.com',
        [user_email],
        fail_silently=False,
    )


def send_email_change_pwd(user_email, user_password):
    send_mail(
        _("Вход на kaifschool.ru"),
        _("Ваш новый пароль для входа: ") + user_password,
        'kaifschoola@gmail.com',
        [user_email],
        fail_silently=False,
    )
