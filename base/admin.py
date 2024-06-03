from django.contrib import admin
from .models import Contact, About


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'email')
    search_fields = ['first_name']
    list_display_links = ['id', 'first_name']


class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'email')
    search_fields = ['title']
    list_display_links = ['id', 'title']


admin.site.register(Contact, ContactAdmin)
admin.site.register(About, AboutAdmin)
