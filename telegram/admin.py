from django.contrib import admin
from .models import TelegramUser, Saved


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'balance', 'is_subscribed']
    list_display_links = ['id', 'username']
    search_fields = ['username', 'first_name', 'last_name']


class SavedAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'title']
    list_display_links = ['id', 'username']
    search_fields = ['username']

    def username(self, obj):
        return obj.user.username

    def title(self, obj):
        return obj.movie.title


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Saved, SavedAdmin)
