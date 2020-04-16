from django.contrib import admin

from .models import *


class LesionAdmin(admin.TabularInline):
    model = Lesion
    min_num = 0
    max_num = 4


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "patient_id", "mri_date", "lesion_num", "psa_level", "ece", "svi")

    inlines = [LesionAdmin]

    def lesion_num(self, e):
        return e.lesions.count()
    lesion_num.short_description = "Number of lesions"


