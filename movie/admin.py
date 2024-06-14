from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Genre,
    Actor,
    Director,
    Saved,
    Comment,
    Movie,
    Country
)


class MovieImageAdmin(admin.ModelAdmin):
    list_display = ('images', 'preview')

    def preview(self, obj):
        return format_html(f"<img width=50 height=50 src='{obj.image.url}'")


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview')
    list_display_links = ('id', 'name')

    def preview(self, obj):
        return format_html(f"<img width=50 height=50 src='{obj.image.url}'")


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview')
    list_display_links = ('id', 'name')

    def preview(self, obj):
        return format_html(f"<img width=50 height=50 src='{obj.image.url}'")


class SavedAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie',)
    list_display_links = ('id', 'movie',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview', 'release_date')
    list_display_links = ('id', 'title')

    def preview(self, obj):
        return format_html(f"<img width=50 height=50 src='{obj.image.url}'")


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Saved, SavedAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country, CountryAdmin)
