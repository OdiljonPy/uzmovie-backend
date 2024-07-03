from modeltranslation.translator import translator, TranslationOptions
from .models import About


class AboutTranslationOptions(TranslationOptions):
    fields = ('location', )


translator.register(About, AboutTranslationOptions)
