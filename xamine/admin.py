from django.contrib import admin

from xamine.models import Patient, Level, AppSetting, Order

admin.site.register(Patient)
admin.site.register(Level)
admin.site.register(AppSetting)
admin.site.register(Order)
