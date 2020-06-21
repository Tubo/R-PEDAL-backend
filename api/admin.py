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
    list_display = ["patient", "psma_date", "lesion_num", "comments", "timestamp"]
    inlines = [PsmaLesionAdmin]

    def lesion_num(self, e):
        return e.lesions.count()

    lesion_num.short_description = "Number of lesions"


class PathologyLesionAdmin(admin.TabularInline):
    model = PathologyLesion
    min_num = 0
    max_num = 2


@admin.register(PathologyEntry)
class PathologyAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "procedure_date",
        "lesion_num",
        "specimen_type",
        "comments",
        "timestamp",
    ]
    inlines = [PathologyLesionAdmin]

    def lesion_num(self, e):
        return e.lesions.count()

    lesion_num.short_description = "Number of lesions"


@admin.register(PiradLocation)
class PiradLocationAdmin(admin.ModelAdmin):
    list_display = [
        "label",
        "mri_lesion_count",
        "psma_lesion_count",
    ]

    ordering = ["label"]

    def mri_lesion_count(self, e):
        return e.mrilesion_set.count()

    mri_lesion_count.short_description = "Number of MRI lesions"

    def psma_lesion_count(self, e):
        return e.psmalesion_set.count()

    psma_lesion_count.short_description = "Number of PSMA lesions"


admin.site.register(Patient)
