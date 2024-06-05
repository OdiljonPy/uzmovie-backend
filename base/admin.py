from django.contrib import admin
from liststyle import   ListStyleAdminMixin
from .models import Contact, About


class ContactAdmin(admin.ModelAdmin, ListStyleAdminMixin):
    list_display = ('id', 'first_name', 'phone_number', 'is_solved', 'status')
    search_fields = ['first_name']
    list_display_links = ['id', 'first_name']
    list_editable = ['is_solved', 'status']
    actions = ('contact_status_published',)

    def contact_status_published(self, request, queryset):
        count = queryset.update(is_solved=True)
        self.message_user(request, "{} contact has been published.".format(count))

    contact_status_published.short_description = 'Mark selected as published'

    def status_colour(self, obj, index):
        if obj.status == "sent to check":
            return 'red'
        elif obj.status == "in progress":
            return 'yellow'
        else:
            return 'green'

    status_colour.allow_tags = True


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'email')
    search_fields = ['phone_number']
    list_display_links = ['id', 'phone_number']


admin.site.register(Contact, ContactAdmin)
admin.site.register(About, AboutUsAdmin)
