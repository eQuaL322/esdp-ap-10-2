from django.test import TestCase
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class TestTask(TestCase):
    def setUp(self) -> None:
        self.driver = Chrome()

    def login(self):
        self.driver.get('http://localhost:8000/ru/')
        self.driver.find_element(By.NAME, 'email').send_keys('jack@gmail.com')
        self.driver.find_element(By.NAME, 'password').send_keys('root')
        self.driver.find_element(By.CLASS_NAME, 'main-style-button').click()
        sleep(1)
        self.assertEqual('http://localhost:8000/ru/', self.driver.current_url)

    def navigate_to_exercise(self):
        self.driver.find_element(By.LINK_TEXT, 'Материалы').click()
        sleep(1)
        self.driver.find_element(By.CLASS_NAME, 'test-ex').click()
        sleep(1)
        self.driver.find_element(By.CLASS_NAME, 'test-ex-link').click()
        sleep(1)

    def create_task(self):
        self.driver.find_element(By.LINK_TEXT, 'Добавить задание').click()
        sleep(1)
        self.driver.find_element(By.ID, 'id_question').send_keys('test_question')
        sleep(1)
        self.driver.find_element(By.ID, 'id_task_type').click()
        sleep(1)
        Select(self.driver.find_element(By.ID, 'id_task_type')).select_by_visible_text('video')
        sleep(1)
        self.driver.find_element(By.ID, 'id_url').send_keys('https://youtube.com/embed/by1QAoRcc-U')
        sleep(1)
        element = self.driver.find_element(By.CLASS_NAME, 'main-style-button')
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script("arguments[0].click();", element)
        sleep(1)

    def update_task(self):
        element = self.driver.find_element(By.CLASS_NAME, 'task-three-dots')
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script("arguments[0].click();", element)
        sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Редактировать').click()
        sleep(1)
        self.driver.find_element(By.ID, 'id_question').send_keys(' updated_question')
        sleep(1)
        element = self.driver.find_element(By.CLASS_NAME, 'main-style-button')
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script("arguments[0].click();", element)
        sleep(1)

    def delete_task(self):
        element = self.driver.find_element(By.CLASS_NAME, 'task-three-dots')
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script("arguments[0].click();", element)
        sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Удалить').click()
        sleep(1)

    def test_task_create(self):
        self.login()
        self.navigate_to_exercise()
        self.create_task()

    def test_task_update(self):
        self.login()
        self.navigate_to_exercise()
        self.update_task()

    def test_task_delete(self):
        self.login()
        self.navigate_to_exercise()
        self.delete_task()

    def tearDown(self) -> None:
        self.driver.close()
