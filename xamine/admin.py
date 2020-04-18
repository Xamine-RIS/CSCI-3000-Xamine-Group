from django.contrib import admin

from xamine.models import Patient, Level, AppSetting, Order, Image, ModalityOption, Team

admin.site.register(Patient)
admin.site.register(Level)
admin.site.register(AppSetting)
admin.site.register(Order)
admin.site.register(Image)
admin.site.register(ModalityOption)  # temp
admin.site.register(Team)