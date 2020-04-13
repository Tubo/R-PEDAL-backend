from django.db import models


class Entry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    patient_id = models.CharField("patient ID", max_length=50)
    mri_date = models.DateField()
    psa_level = models.IntegerField()
    ece = models.BooleanField()
    svi_choices = (
        ("NO", "No"),
        ("LEFT", "Yes - left"),
        ("RIGHT", "Yes - right"),
        ("BILATERAL", "Yes - bilateral"),
    )
    svi = models.CharField(max_length=20)
    comments = models.TextField(blank=True)


class Lesion(models.Model):
    name = models.CharField(
        choices=(("index", "Index lesion"), ("additional", "Additional lesion")),
        max_length=10,
    )
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="lesions")
    locations = models.ManyToManyField("Location")
    size = models.IntegerField()
    adc = models.IntegerField()
    score_choices = (("5", "5"), ("4", "4"), ("3", "3"), ("2", "2"))
    score = models.CharField("PIRADS 2.1 score", choices=score_choices, max_length=2)
    upgraded_choice = (
        ("NO", "No"),
        ("PZ DCE", "Yes - PZ DCE"),
        ("TZ DWI", "Yes - TZ DWI"),
    )
    upgraded = models.CharField(
        "PIRADS 2.1 upgraded", max_length=20, choices=upgraded_choice
    )


class LocationManager(models.Manager):
    def get_location_from_str(self, name: str):
        queryset = self.get_queryset()
        if name.lower() == "urethra":
            return queryset.get(zone__iexact="urethra")
        parts = name.split("_")
        if parts[-1] == "sv":
            return queryset.get(laterality__iexact=parts[0], zone__iexact="sv")
        else:
            return queryset.get(
                laterality__iexact=parts[0],
                level__iexact=parts[1],
                zone__iexact=parts[2],
            )


class Location(models.Model):
    laterality = models.CharField(
        null=True, blank=True, choices=(("L", "Left"), ("R", "Right")), max_length=5,
    )
    level_choices = (
        ("URETHRA", "Urethra"),
        ("APEX", "Apex"),
        ("MID", "Mid"),
        ("BASE", "Base"),
        ("SV", "Seminal vesicles"),
    )
    level = models.CharField(choices=level_choices, max_length=10,)
    zone_choices = (
        ("PZa", "PZ anterior"),
        ("PZpl", "PZ posterolateral"),
        ("PZpm", "PZ posteromedial"),
        ("CZ", "CZ"),
        ("TZa", "TZ anterior"),
        ("TZp", "TZ posterior"),
        ("AFS", "Anterior fibromuscular stroma"),
        ("URETHRA", "Urethra"),
        ("SV", "Seminal vesicles"),
    )
    zone = models.CharField(choices=zone_choices, max_length=10,)

    objects = LocationManager()

    class Meta:
        unique_together = ["laterality", "level", "zone"]

    def __str__(self):
        lateral = self.get_laterality_display() or ""
        level = self.get_level_display()
        zone = self.get_zone_display()

        if level == zone:
            return f"{level}" if not lateral else f"{lateral} {level}"
        return f"{lateral} {level} {zone}"
