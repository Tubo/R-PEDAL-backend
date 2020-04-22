from rest_framework import serializers as s
from .models import *

locations = [
    "l_base_cz",
    "l_sv",
    "l_apex_pza",
    "l_apex_pzpl",
    "l_apex_pzpm",
    "l_apex_tza",
    "l_apex_tzp",
    "l_apex_afs",
    "l_mid_pza",
    "l_mid_pzpl",
    "l_mid_pzpm",
    "l_mid_tza",
    "l_mid_tzp",
    "l_mid_afs",
    "l_base_pza",
    "l_base_pzpl",
    "l_base_pzpm",
    "l_base_tza",
    "l_base_tzp",
    "l_base_afs",
    "r_base_cz",
    "r_sv",
    "r_apex_pza",
    "r_apex_pzpl",
    "r_apex_pzpm",
    "r_apex_tza",
    "r_apex_tzp",
    "r_apex_afs",
    "r_mid_pza",
    "r_mid_pzpl",
    "r_mid_pzpm",
    "r_mid_tza",
    "r_mid_tzp",
    "r_mid_afs",
    "r_base_pza",
    "r_base_pzpl",
    "r_base_pzpm",
    "r_base_tza",
    "r_base_tzp",
    "r_base_afs",
    "urethra",
]


class MriLesionSerializer(s.ModelSerializer):
    locations = s.ListField(
        child=s.ChoiceField(choices=locations), allow_empty=False, max_length=4, write_only=True
    )

    class Meta:
        model = MriLesion
        fields = ["locations", "size", "adc", "score", "upgraded"]


class MriEntrySerializer(s.ModelSerializer):
    patient_id = s.CharField()
    lesions = MriLesionSerializer(many=True)

    class Meta:
        model = MriEntry
        fields = [
            "timestamp",
            "patient_id",
            "mri_date",
            "psa_level",
            "ece",
            "svi",
            "comments",
            "lesions",
        ]
        depth = 1
        read_only_fields = ["timestamp"]

    def create(self, validated_data):
        patient_id = validated_data.pop("patient_id")
        lesion_data = validated_data.pop("lesions")
        (patient, _) = Patient.objects.get_or_create(patient_id=patient_id)
        e = MriEntry.objects.create(**validated_data, patient=patient)
        for lesion in lesion_data:
            location_data = lesion.pop("locations")
            locations = map(Location.objects.get_location_from_str, location_data)
            new_lesion = MriLesion.objects.create(**lesion, entry=e)
            new_lesion.locations.add(*list(locations))
        return e



