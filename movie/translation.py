from modeltranslation.translator import translator, TranslationOptions
from .models import Movie, Genre


class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)


class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Movie, MovieTranslationOptions)
translator.register(Genre, GenreTranslationOptions)
