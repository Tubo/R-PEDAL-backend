from rest_framework import serializers as s
from .models import *


class MriLesionSerializer(s.ModelSerializer):
    locations = s.ListField(child=s.CharField(), allow_empty=False, max_length=4, write_only=True)

    class Meta:
        model = MriLesion
        exclude = [
            "entry",
        ]


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
        patient_data = validated_data.pop("patient_id")
        lesion_data = validated_data.pop("lesions")
        p = Patient.objects.get_or_create(**patient_data)
        e = MriEntry.objects.create(**validated_data, patient=p)
        for lesion in lesion_data:
            location_data = lesion.pop("locations")
            locations = map(Location.objects.get_location_from_str, location_data)
            new_lesion = MriLesion.objects.create(**lesion, entry=e)
            new_lesion.locations.add(*list(locations))
        return e
