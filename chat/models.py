from django.db import models
from django.utils import timezone
from accounts.models import Account


class ChatMessage(models.Model):
    sender = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Отправитель'
    )
    recipient = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='Получатель'
    )
    message = models.TextField(verbose_name='Сообщение')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'

    def __str__(self):
        return f'{self.sender} -> {self.recipient}'
