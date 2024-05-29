from django.contrib import admin
from .models import Status, Choice, Subscription, ChoiceOTP, Balance_service, Card


admin.site.register(Balance_service)
admin.site.register(Card)
admin.site.register(Status)
admin.site.register(Choice)
admin.site.register(ChoiceOTP)
admin.site.register(Subscription)
