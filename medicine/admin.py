from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
class DayInline(admin.TabularInline):
    model = MedicineDay
class MedicineAdmin(admin.ModelAdmin):
    inlines = (DayInline, )
admin.site.register(Medicine, MedicineAdmin)
