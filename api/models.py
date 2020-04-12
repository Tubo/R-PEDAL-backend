from django.db import models


class Entry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    patient_id = models.CharField("patient ID", max_length=50)
    mri_date = models.DateField()
    psa_level = models.IntegerField()
    ece = models.BooleanField()
    svi = models.CharField(max_length=20)
    comments = models.TextField()


class Lesion(models.Model):
    name = models.CharField(
        choices=(("IND", "Index lesion"), ("ADD", "Additional lesion")), max_length=10
    )
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="lesions")
    locations = models.ManyToManyField("Location")
    size = models.IntegerField()
    adc = models.IntegerField()
    score = models.CharField("PIRADS 2.1 score", max_length=5)
    upgraded = models.CharField("PIRADS 2.1 upgraded", max_length=20)


class Location(models.Model):
    laterality = models.CharField(
        null=True,
        blank=True,
        choices=(("LEFT", "Left"), ("RIGHT", "Right")),
        max_length=5,
    )
    level_choices = (
            ("URETHRA", "Urethra"),
            ("APEX", "Apex"),
            ("MID", "Mid"),
            ("BASE", "Base"),
            ("SV", "Seminal vesicles"),
        )
    level = models.CharField(
        choices=level_choices,
        max_length=10,
    )
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
    zone = models.CharField(
        choices=zone_choices,
        max_length=10,
    )

    class Meta:
        unique_together = ['laterality', 'level', 'zone']

    def __str__(self):
        lateral = self.get_laterality_display() or ""
        level = self.get_level_display()
        zone = self.get_zone_display()

        if level == zone:
            return f"{lateral} {level}"
        return f"{lateral} {level} {zone}"
