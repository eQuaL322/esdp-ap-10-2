# Generated by Django 4.2 on 2023-05-22 12:02

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bio_text_en',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='БИО'),
        ),
        migrations.AddField(
            model_name='account',
            name='bio_text_ru',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='БИО'),
        ),
        migrations.AddField(
            model_name='account',
            name='first_name_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='account',
            name='first_name_ru',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='account',
            name='last_name_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='account',
            name='last_name_ru',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True, verbose_name='Телефон'),
        ),
    ]