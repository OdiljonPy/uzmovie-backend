from django.contrib import admin

from .models import Choice, Subscription, ChoiceOTP, Card


admin.site.register(Card)
admin.site.register(Choice)
admin.site.register(ChoiceOTP)
admin.site.register(Subscription)
