from django.contrib import admin
from .models import (
    Genre,
    Actor,
    Director,
    Saved,
    Comment,
    Movie,
    Country,
    Language
)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class SavedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'imdb_rating')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Saved, SavedAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country, CountryAdmin)
