from django.db import models

pirad_locations = [
    ("l_base_cz", "l_base_cz"),
    ("l_sv", "l_sv"),
    ("l_apex_pza", "l_apex_pza"),
    ("l_apex_pzpl", "l_apex_pzpl"),
    ("l_apex_pzpm", "l_apex_pzpm"),
    ("l_apex_tza", "l_apex_tza"),
    ("l_apex_tzp", "l_apex_tzp"),
    ("l_apex_afs", "l_apex_afs"),
    ("l_mid_pza", "l_mid_pza"),
    ("l_mid_pzpl", "l_mid_pzpl"),
    ("l_mid_pzpm", "l_mid_pzpm"),
    ("l_mid_tza", "l_mid_tza"),
    ("l_mid_tzp", "l_mid_tzp"),
    ("l_mid_afs", "l_mid_afs"),
    ("l_base_pza", "l_base_pza"),
    ("l_base_pzpl", "l_base_pzpl"),
    ("l_base_pzpm", "l_base_pzpm"),
    ("l_base_tza", "l_base_tza"),
    ("l_base_tzp", "l_base_tzp"),
    ("l_base_afs", "l_base_afs"),
    ("r_base_cz", "r_base_cz"),
    ("r_sv", "r_sv"),
    ("r_apex_pza", "r_apex_pza"),
    ("r_apex_pzpl", "r_apex_pzpl"),
    ("r_apex_pzpm", "r_apex_pzpm"),
    ("r_apex_tza", "r_apex_tza"),
    ("r_apex_tzp", "r_apex_tzp"),
    ("r_apex_afs", "r_apex_afs"),
    ("r_mid_pza", "r_mid_pza"),
    ("r_mid_pzpl", "r_mid_pzpl"),
    ("r_mid_pzpm", "r_mid_pzpm"),
    ("r_mid_tza", "r_mid_tza"),
    ("r_mid_tzp", "r_mid_tzp"),
    ("r_mid_afs", "r_mid_afs"),
    ("r_base_pza", "r_base_pza"),
    ("r_base_pzpl", "r_base_pzpl"),
    ("r_base_pzpm", "r_base_pzpm"),
    ("r_base_tza", "r_base_tza"),
    ("r_base_tzp", "r_base_tzp"),
    ("r_base_afs", "r_base_afs"),
    ("urethra", "urethra"),
]


class Patient(models.Model):
    patient_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.patient_id


class PiradLocation(models.Model):
    label = models.CharField("Location", max_length=20, choices=pirad_locations)


class MriEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="mri_entries"
    )
    mri_date = models.DateField("MRI date")
    psa_level = models.DecimalField("PSA level", max_digits=6, decimal_places=2)
    ece = models.BooleanField("ECE")
    svi_choices = (
        ("NO", "No"),
        ("LEFT", "Yes - left"),
        ("RIGHT", "Yes - right"),
        ("BILATERAL", "Yes - bilateral"),
    )
    svi = models.CharField("SVI", max_length=20, choices=svi_choices)
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "entries"


class MriLesion(models.Model):
    entry = models.ForeignKey(
        MriEntry, on_delete=models.CASCADE, related_name="lesions"
    )
    is_index = models.BooleanField("Index lesion?")
    locations = models.ManyToManyField(PiradLocation)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    adc = models.IntegerField("ADC")
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


class PsmaEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="psma_entries"
    )
    psma_date = models.DateField("PSMA date")
    comments = models.TextField(blank=True)


class PsmaLesion(models.Model):
    entry = models.ForeignKey(
        PsmaEntry, on_delete=models.CASCADE, related_name="lesions"
    )
    is_index = models.BooleanField("Index lesion?", default=False)
    locations = models.ManyToManyField(PiradLocation)
    suv = models.DecimalField("SUV", max_digits=6, decimal_places=2)


class PathologyEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="pathology_entries"
    )
    procedure_date = models.DateField("Procedure date")
    specimen_type = models.CharField(
        "Specimen type",
        choices=(("BIOPSY", "Biopsy"), ("PROSTATECTOMY", "Prostatectomy")),
        max_length=20,
    )
    comments = models.TextField(blank=True)


class PathologyLesion(models.Model):
    entry = models.ForeignKey(
        PathologyEntry, on_delete=models.CASCADE, related_name="lesions"
    )
    is_index = models.BooleanField("Index lesion?", default=False)
    grade = models.CharField(
        "Lesion grade",
        max_length=10,
        choices=(
            ("ISUP 1", "ISUP 1"),
            ("ISUP 2", "ISUP 2"),
            ("ISUP 3", "ISUP 3"),
            ("ISUP 4", "ISUP 4"),
            ("ISUP 5", "ISUP 5"),
            ("NONE", "No malignancy"),
        ),
    )
    greatest_percentage = models.DecimalField(
        "Greatest percentage of cancer", null=True, max_digits=5, decimal_places=2

    )
    positive_core = models.IntegerField("Positive core number", null=True)
    total_core = models.IntegerField("Total core number", null=True)
    lesion_size = models.DecimalField("Lesion size", null=True, max_digits=6, decimal_places=2)
    loc_side = models.CharField(
        "Side of prostate",
        max_length=10,
        choices=(("RIGHT", "Right"), ("LEFT", "Left"), ("NA", "Not stated")),
    )
    loc_zone = models.CharField(
        "Zone of prostate",
        choices=(("BASE", "Base"), ("MID", "Mid"), ("APEX", "Apex"), ("NA", "Not stated")),
        max_length=5,
    )
