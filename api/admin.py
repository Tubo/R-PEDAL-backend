from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *


class EntryResource(resources.Resource):
    class Meta:
        model = MriEntry
        exclude = ("id",)
        export_order = (
            "timestamp",
            "patient_id",
            "mri_date",
            "psa_level",
            "ece",
            "svi",
            "comments",
        )


class MriLesionAdmin(admin.TabularInline):
    model = MriLesion
    min_num = 0
    max_num = 2


@admin.register(MriEntry)
class MriEntryAdmin(ImportExportModelAdmin):
    list_display = (
        "timestamp",
        "patient_id",
        "mri_date",
        "lesion_num",
        "psa_level",
        "ece",
        "svi",
        "comments",
    )

    inlines = [MriLesionAdmin]

    def lesion_num(self, e):
        return e.lesions.count()

    lesion_num.short_description = "Number of lesions"
