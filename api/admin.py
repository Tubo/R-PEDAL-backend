from django.contrib import admin

from .models import *


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesion)
class LesionAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("laterality", "level", "zone")
