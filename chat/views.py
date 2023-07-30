from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils import timezone
from accounts.models import Account
from .models import ChatMessage
from django.utils.translation import gettext_lazy as _


@login_required
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        sender = request.user
        recipient = Account.objects.filter(role='Technical-support').first()
        response = ChatMessage.objects.create(sender=sender, recipient=recipient, message=message)
        messages.success(request, _('Ваше сообщение успешно отправлено. Мы ответим вам на Ваш email'))
        response.save()

        email_subject = 'Новое сообщение в ТехПоддержку'
        email_body = f'Имя пользователя: {sender.first_name} {sender.last_name}\n' \
                     f'Роль пользователя: {sender.role}\n' \
                     f'Email пользователя: {sender.email}\n' \
                     f'Текст сообщения: {message}\n' \
                     f'Время отправки: {timezone.now().strftime("%d.%m.%Y %H:%M")}'
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.SUPPORT_EMAIL],
            fail_silently=False,
        )
    return redirect(request.META.get('HTTP_REFERER'))
