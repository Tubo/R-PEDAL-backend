from rest_framework import serializers as s
from .models import *


class LesionSerializer(s.ModelSerializer):
    locations = s.ListField(child=s.CharField(), allow_empty=False, max_length=4, write_only=True)
    read_location = s.StringRelatedField(source="locations", many=True, read_only=True)

    class Meta:
        model = Lesion
        exclude = [
            "entry",
        ]


class EntrySerializer(s.ModelSerializer):
    lesions = LesionSerializer(many=True)

    class Meta:
        model = Entry
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
        lesion_data = validated_data.pop("lesions")
        e = Entry.objects.create(**validated_data)
        for lesion in lesion_data:
            location_data = lesion.pop("locations")
            locations = map(Location.objects.get_location_from_str, location_data)
            new_lesion = Lesion.objects.create(**lesion, entry=e)
            new_lesion.locations.add(*list(locations))
        return e
