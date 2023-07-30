from django.contrib import admin
from .models import Account
from modeltranslation.admin import TranslationAdmin


class AccountAdmin(TranslationAdmin):
    list_display = ('username',)


admin.site.register(Account, AccountAdmin)
