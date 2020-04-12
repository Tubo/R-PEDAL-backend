from django.contrib import admin

from .models import *


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('laterality', 'level', 'zone')
