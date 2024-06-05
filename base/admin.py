from django.contrib import admin
from .models import Contact, About, DefaultStatus


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'is_solved')
    search_fields = ['first_name']
    list_display_links = ['id', 'first_name']
    actions = ('contact_status_published',)

    def contact_status_published(self, request, queryset):
        count = queryset.update(is_solved=True)
        self.message_user(request, "{} contact has been published.".format(count))

    contact_status_published.short_description = 'Mark selected as published'


class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'email')
    search_fields = ['title']
    list_display_links = ['id', 'title']


admin.site.register(Contact, ContactAdmin)
admin.site.register(About, AboutAdmin)
