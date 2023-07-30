from selenium.webdriver import Chrome
from django.test import TestCase
from time import sleep
from selenium.webdriver.common.by import By


class TestLogIn(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def test_login(self):
        self.driver.get('http://localhost:8000/ru/')
        self.driver.find_element('name', 'email').send_keys('admin@gmail.com')
        self.driver.find_element('name', 'password').send_keys('root')
        self.driver.find_element(By.CLASS_NAME, 'auth-button').click()
        sleep(5)
        self.assertEqual('http://localhost:8000/ru/', self.driver.current_url)

    def tearDown(self) -> None:
        self.driver.close()
