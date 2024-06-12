from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, About


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'is_solved', 'status_colored')
    search_fields = ['first_name']
    list_display_links = ['id', 'first_name']
    list_editable = ['is_solved']
    actions = ('contact_status_published',)

    def status_colored(self, obj):
        status_colors = {
            1: 'red',
            2: 'yellow',
            3: 'green',
        }
        color = status_colors.get(obj.status)
        return format_html(f'<span style="color: {color};">{obj.get_status_display()}</span>')

    status_colored.short_description = 'Status'

    def contact_status_published(self, request, queryset):
        count = queryset.update(is_solved=True)
        self.message_user(request, "{} contact has been published.".format(count))

    contact_status_published.short_description = 'Mark selected as published'


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'email')
    search_fields = ['phone_number']
    list_display_links = ['id', 'phone_number']


admin.site.register(Contact, ContactAdmin)
admin.site.register(About, AboutUsAdmin)
