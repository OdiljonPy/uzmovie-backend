from django.contrib import admin
from .models import Balance_service, Cards, Status, Choice, Subscription, ChoiceOTP


admin.site.register(Balance_service)
admin.site.register(Cards)
admin.site.register(Status)
admin.site.register(Choice)
admin.site.register(ChoiceOTP)
admin.site.register(Subscription)
