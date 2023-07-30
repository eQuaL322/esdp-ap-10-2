from django.test import TestCase
from django.urls import reverse
from ..models import Account


class TestRegister(TestCase):
    def setUp(self) -> None:
        self.register_url = '/ru/auth/register/'

        # Пробные данные
        self.user = {
            'username': 'email@gmail.com',
            'email': 'email@gmail.com',
            'role': 'Student',
            'timezone': 'Asia/Almaty',
            'password': 'root',
            'password_confirm': 'root'
        }

    def test_register(self):
        # Имитация запроса POST с данными пользователя
        response = self.client.post(self.register_url, self.user)

        # Проверяем, прошла ли регистрация успешно (HTTP 302 - Redirect)
        self.assertEqual(response.status_code, 302)

        # Проверить, был ли пользователь создан в базе данных
        self.assertTrue(Account.objects.filter(email=self.user['email']).exists())

        # Получить объект пользователя из базы данных
        user = Account.objects.get(email=self.user['email'])

        # Проверка правильность адреса электронной почты пользователя
        self.assertEqual(user.email, self.user['email'])

        # Проверка правильность пароля пользователя
        self.assertTrue(user.check_password(self.user['password']))
