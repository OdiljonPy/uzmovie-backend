from django.contrib import admin
from .models import TelegramUser


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'balance', 'is_subscribed']
    list_display_links = ['id', 'username']
    search_fields = ['username', 'first_name', 'last_name']


admin.site.register(TelegramUser, TelegramUserAdmin)
