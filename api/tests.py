from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.test import APITestCase

from .models import *
from .serializers import *


def mri_lesion_builder(
    location_set: int = 1,
    size: int = 10,
    adc: int = 500,
    score: str = "2",
    upgraded: str = "NO",
):
    locations = [
        [],
        ["r_mid_pzpm"],
        ["l_apex_pzpl", "urethra"],
        ["l_apex_pzpl", "urethra", "r_mid_pzpm"],
        ["l_apex_pzpl", "urethra", "r_mid_pzpm", "l_vs"],
        ["l_apex_pzpl", "urethra", "r_mid_pzpm", "this should not be here"],
    ]
    return {
        "locations": locations[location_set],
        "size": size,
        "adc": adc,
        "score": score,
        "upgraded": upgraded,
    }


def mri_form_builder(lesions: list, date="2020-04-01", patient_id="X123"):
    return {
        "patient_id": patient_id,
        "mri_date": date,
        "psa_level": 15,
        "lesions": lesions,
        "ece": "NO",
        "svi": "NO",
        "comments": "No comments",
    }


class TestViews(APITestCase):
    def test_post_mri_good_form(self):
        # A new POST request is sent to MRI api
        self.client.post(reverse("mri-entry"), data=mri_form_builder([]), format="json")

        self.assertEqual(1, Patient.objects.count(), "A new Patient should be created")
        self.assertEqual(
            1, MriEntry.objects.count(), "A new MRI Entry should be created"
        )
        self.assertEqual(
            0, MriLesion.objects.count(), "No MRI Lesions should be created"
        )

        # Send a second POST request with the same user info
        self.client.post(reverse("mri-entry"), data=mri_form_builder([]), format="json")
        self.assertEqual(
            1, Patient.objects.count(), "The patient count should still be one"
        )
        self.assertEqual(
            2, MriEntry.objects.count(), "A new MRI Entry should be created (2)"
        )
        self.assertEqual(
            0, MriLesion.objects.count(), "No MRI Lesions should be created"
        )

        # Send a third POST request with same user info, this time add lesion info
        r = self.client.post(
            reverse("mri-entry"),
            data=mri_form_builder([mri_lesion_builder(location_set=1)]),
            format="json",
        )
        self.assertEqual(
            1, Patient.objects.count(), "The patient count should still be one"
        )
        self.assertEqual(3, MriEntry.objects.count(), r.data)
        self.assertEqual(
            1, MriLesion.objects.count(), "One new MRI Lesions should be created"
        )

    def test_post_mri_bad_form(self):
        pass
