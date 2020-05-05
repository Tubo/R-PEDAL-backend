from django.contrib import admin

from .models import *


class MriLesionAdmin(admin.TabularInline):
    model = MriLesion
    min_num = 0
    max_num = 2


@admin.register(MriEntry)
class MriEntryAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "mri_date",
        "lesion_num",
        "psa_level",
        "ece",
        "svi",
        "comments",
        "timestamp",
    )

    inlines = [MriLesionAdmin]

    def lesion_num(self, e):
        return e.lesions.count()

    lesion_num.short_description = "Number of lesions"


class PsmaLesionAdmin(admin.TabularInline):
    model = PsmaLesion
    min_num = 0
    max_num = 2


@admin.register(PsmaEntry)
class PsmaEntryAdmin(admin.ModelAdmin):
    inlines = [PsmaLesionAdmin]


class PathologyLesionAdmin(admin.TabularInline):
    model = PathologyLesion
    min_num = 0
    max_num = 2


@admin.register(PathologyEntry)
class PathologyAdmin(admin.ModelAdmin):
    inlines = [PathologyLesionAdmin]


admin.site.register(PiradLocation)
admin.site.register(Patient)
