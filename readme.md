Как создать ветку от тикета:
1. Переходим на страницу задачи
2. жмем на галочку опций кнопки create merge и там выбираем Create branch
3. указываем имя ветки - по умолчанию будет предлагатся соответственно названию задания, Вам же нужно вначале указать действие которое будете производить с приложением - добавить функционал - feature, улучшить внешний вид - frontend, исправить баги - bugfix, улучшить код - refactor. Итого название ветки например с добавлением модели lesson будет примерно таким - feature-lesson 
Внимание! Используйте для раздерения названий только дефис.
4. Жмем кнопку создать. 
5. Переходим на новосозданную ветку. Все коммиты будут автоматически привязыватся к ней. Но если создать еще одну ветку от этой задачи - придется уже вручную проставлять номер задачи.

Тестовые учетки:

superuser
логин: admin@gmail.com
пароль: root

admin
логин: jane@gmail.com
пароль: root

teacher
логин: jack@gmail.com, blake@gmail.com
пароль: root

student
логин: sara@gmail.com, pip@gmail.com
пароль: root

curator
логин: bob@gmail.com
пароль: root

supervisor
логин: john@gmail.com
пароль: root

marathon-curator
логин: tim@gmail.com
пароль: root

content-maker
логин: minho@gmail.com
пароль: root

technical-support
логин: tomas@gmail.com
пароль: root

тестовая почта школы
логин: kaifschoola@gmail.com
пароль: 4MNzX93Clr@a
пароль приложения: zgsjrpiagmfihihe

Чтобы локально запустить celery без докер контейнера:
celery -A core beat -l info
celery -A core worker -l info

Чтобы локально запустить celery из docker-compose:
- Первый запуск
docker-compose up --build

- Последующие запуски
docker-compose up