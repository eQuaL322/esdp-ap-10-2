from modeltranslation.translator import translator, TranslationOptions
from .models import Account


class AccountTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'bio_text')


translator.register(Account, AccountTranslationOptions)
