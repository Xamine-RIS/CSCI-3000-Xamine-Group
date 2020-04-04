from django.contrib import admin

from xamine.models import Patient, Level, AppSetting

admin.site.register(Patient)
admin.site.register(Level)
admin.site.register(AppSetting)
