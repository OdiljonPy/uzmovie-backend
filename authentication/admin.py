from django.contrib import admin
from .models import User, OTPRegisterResend, OTPSetPassword

admin.site.register(User)
admin.site.register(OTPRegisterResend)
admin.site.register(OTPSetPassword)
