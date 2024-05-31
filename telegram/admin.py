from django.contrib import admin
from .models import TelegramUser, Saved


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'balance', 'is_subscribed']
    list_display_links = ['id', 'chat_id']
    search_fields = ['chat_id']


class SavedAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'title']
    list_display_links = ['id', 'chat_id']
    search_fields = ['chat_id', 'title']

    def chat_id(self, obj):
        return obj.user.chat_id

    def title(self, obj):
        return obj.movie.title


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Saved, SavedAdmin)
