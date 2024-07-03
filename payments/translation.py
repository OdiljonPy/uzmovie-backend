from modeltranslation.translator import translator, TranslationOptions
from .models import Choice


class ChoiceTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


translator.register(Choice, ChoiceTranslationOptions)
