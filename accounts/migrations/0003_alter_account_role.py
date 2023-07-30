# Generated by Django 4.2 on 2023-05-29 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_bio_text_en_account_bio_text_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('Admin', 'Админ'), ('Teacher', 'Учитель'), ('Student', 'Ученик'), ('Curator', 'Куратор'), ('Supervisor', 'Руководитель'), ('Marathon-curator', 'Куратор-марафонов'), ('Content-maker', 'Контент-мейкер'), ('Technical-support', 'Техподдержка')], max_length=200, verbose_name='Роль'),
        ),
    ]
