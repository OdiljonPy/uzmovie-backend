from django.contrib import admin
from .models import User, OTPRegisterResend


admin.site.register(User)
admin.site.register(OTPRegisterResend)
