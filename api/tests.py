from django.test import TestCase
from rest_framework.test import APITestCase

from .models import *
from .serializers import *


test_entry_1 = {
            "patient_id": "X123",
            "mri_date": "2020-04-01",
            "psa_level": 10,
            "lesions": [
                {
                    "name": "index",
                    "locations": ["R_mid_PZpm"],
                    "size": 10,
                    "adc": 700,
                    "score": "4",
                    "upgraded": "PZ DCE",
                },
                {
                    "name": "additional",
                    "locations": ["L_apex_PZpl", "Urethra"],
                    "size": 10,
                    "adc": 700,
                    "score": "3",
                    "upgraded": "NO",
                },
            ],
            "ece": "NO",
            "svi": "NO",
            "comments": "marked dwi artefact",
        }

test_entry_2 = {
            "patient_id": "X123",
            "mri_date": "2020-04-01",
            "psa_level": 10,
            "lesions": [],
            "ece": "NO",
            "svi": "NO",
            "comments": "",
        }

class TestSerializers(APITestCase):
    def test_write_entry(self):
        s = EntrySerializer(data=test_entry_1)
        self.assertTrue(s.is_valid(), s.errors)
        e = s.save()
        self.assertEqual(Entry.objects.first(), e)
        self.assertEqual(Lesion.objects.count(), 2)
        self.assertEqual(Lesion.objects.get(name="index").locations.count(), 1)
        self.assertEqual(Lesion.objects.get(name="additional").locations.count(), 2)
        self.assertEqual(Location.objects.filter(lesion__entry=e).count(), 3)


class TestViews(APITestCase):
    def test_list(self):
        r = self.client.get("/")
        self.assertEqual([], r.data)

    def test_create(self):
        r = self.client.post("/", test_entry_1, format='json')
        self.assertEqual(Entry.objects.count(), 1, r.data)
