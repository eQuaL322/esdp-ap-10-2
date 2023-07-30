from django.test import TestCase
from ..models import Account
from django.urls import reverse


class TestLogOut(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(username='email@gmail.com',
                                                email='email@gmail.com',
                                                role='Student',
                                                timezone='Asia/Almaty',
                                                password='root')

    def test_logout(self):
        self.client.login(email='email@gmail.com', password='root')
        response = self.client.get('/ru/auth/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)

    def tearDown(self) -> None:
        self.user.delete()
