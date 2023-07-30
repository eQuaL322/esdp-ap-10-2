from time import sleep
from selenium.webdriver import Chrome
from django.test import TestCase
from selenium.webdriver.common.by import By


class TestExercise(TestCase):
    def setUp(self) -> None:
        self.driver = Chrome()

    def test_signup(self):
        """Авторизация пользователя"""
        self.driver.get('http://localhost:8000/ru/')
        self.driver.find_element(By.NAME, 'email').send_keys('jack@gmail.com')
        self.driver.find_element(By.NAME, 'password').send_keys('root')
        self.driver.find_element(By.CLASS_NAME, 'main-style-button').click()
        self.assertEqual('http://localhost:8000/ru/', self.driver.current_url)

    def to_test_theme(self):
        """Переход к тестовой теме"""
        self.driver.find_element(By.LINK_TEXT, 'Материалы').click()
        sleep(1)
        cards = self.driver.find_elements(By.CLASS_NAME, 'cards')
        for card in cards:
            title = card.find_element(By.CLASS_NAME, 'card-theme-title')
            if "Test" in title.text:
                link = card.find_element(By.TAG_NAME, 'a')
                self.driver.execute_script("arguments[0].click();", link)
                sleep(1)
                break

    def test_exercise_1_create(self):
        self.test_signup()
        self.to_test_theme()
        self.driver.find_element(By.ID, 'add-classwork').click()
        sleep(1)
        self.driver.find_element(By.ID, 'id_title').send_keys('test')
        sleep(1)
        self.driver.find_element(By.ID, 'classwork').click()

    def test_exercise_2_update(self):
        self.test_signup()
        self.to_test_theme()
        self.driver.find_element(By.ID, 'three-dots').click()
        sleep(1)
        self.driver.find_element(By.ID, 'exercise-update').click()
        sleep(1)
        self.driver.find_element(By.ID, 'id_title').send_keys('-update')
        sleep(1)
        self.driver.find_element(By.ID, 'exercise-change').click()

    def test_exercise_3_delete(self):
        self.test_signup()
        self.to_test_theme()
        self.driver.find_element(By.ID, 'three-dots').click()
        sleep(1)
        self.driver.find_element(By.ID, 'exercise-delete').click()
        sleep(1)
        self.driver.find_element(By.ID, 'exercise-confirm-delete').click()

    def tearDown(self) -> None:
        self.driver.close()
