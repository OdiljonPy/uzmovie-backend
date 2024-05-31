from django.contrib import admin

from .models import TelegramUser, Saved


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'balance', 'is_subscribed']
    list_display_links = ['id', 'user_id']
    search_fields = ['user_id']


class SavedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'title']
    list_display_links = ['id', 'user_id']
    search_fields = ['user_id', 'title']

    def user_id(self, obj):
        return obj.user.user_id

    def title(self, obj):
        return obj.movie.title


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Saved, SavedAdmin)
