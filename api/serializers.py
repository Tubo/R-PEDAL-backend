from rest_framework import serializers as s
from .models import *


class MriLesionSerializer(s.ModelSerializer):
    locations = s.ListField(
        child=s.ChoiceField(choices=pirad_locations),
        allow_empty=True,
        max_length=4,
        write_only=True,
    )

    class Meta:
        model = MriLesion
        fields = ["is_index", "locations", "size", "adc", "score", "upgraded"]


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
        patient, _ = Patient.objects.get_or_create(patient_id=patient_id)
        e = MriEntry.objects.create(**validated_data, patient=patient)

        for lesion in lesion_data:
            location_data = lesion.pop("locations", [])
            locations = [
                PiradLocation.objects.get_or_create(label=loc)[0]
                for loc in location_data
            ]
            new_lesion = MriLesion.objects.create(**lesion, entry=e)
            new_lesion.locations.add(*locations)
        return e


class PsmaLesionSerializer(s.ModelSerializer):
    locations = s.ListField(
        child=s.ChoiceField(choices=pirad_locations),
        allow_empty=True,
        max_length=4,
        write_only=True,
    )

    class Meta:
        model = PsmaLesion
        fields = ("is_index", "locations", "suv")


class PsmaEntrySerializer(s.ModelSerializer):
    patient_id = s.CharField()
    lesions = PsmaLesionSerializer(many=True)

    class Meta:
        model = PsmaEntry
        fields = ("timestamp", "patient_id", "lesions", "psma_date", "comments")
        read_only_fields = ("timestamp",)

    def create(self, validated_data):
        patient_id = validated_data.pop("patient_id")
        lesion_data = validated_data.pop("lesions")
        patient, _ = Patient.objects.get_or_create(patient_id=patient_id)
        e = PsmaEntry.objects.create(**validated_data, patient=patient)

        for lesion in lesion_data:
            location_data = lesion.pop("locations", [])
            locations = [
                PiradLocation.objects.get_or_create(label=loc)[0]
                for loc in location_data
            ]
            new_lesion = PsmaLesion.objects.create(**lesion, entry=e)
            new_lesion.locations.add(*locations)
        return e


class PathologyLesionSerializer(s.ModelSerializer):
    class Meta:
        model = PathologyLesion
        fields = (
            "is_index",
            "grade",
            "greatest_percentage",
            "positive_core",
            "total_core",
            "lesion_size",
            "loc_side",
            "loc_zone",
        )


class PathologyEntrySerializer(s.ModelSerializer):
    patient_id = s.CharField()
    lesions = PathologyLesionSerializer(many=True)

    class Meta:
        model = PathologyEntry
        fields = ("timestamp", "patient_id", "procedure_date", "comments", "lesions")
        read_only_fields = ("timestamp",)

    def create(self, validated_data):
        patient_id = validated_data.pop("patient_id")
        lesion_data = validated_data.pop("lesions")
        patient, _ = Patient.objects.get_or_create(patient_id=patient_id)
        e = PathologyEntry.objects.create(**validated_data, patient=patient)

        for lesion in lesion_data:
            PathologyLesion.objects.create(**lesion, entry=e)
        return e
