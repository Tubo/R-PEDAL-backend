from django.shortcuts import reverse
from rest_framework.test import APIClient
import pytest

from .models import *
from .serializers import *

pytestmark = pytest.mark.django_db

pirad_locations_list = [loc[0] for loc in pirad_locations]

locations = [
    [],
    ["r_mid_pzpm"],
    ["l_apex_pzpl", "urethra"],
    ["l_apex_pzpl", "urethra", "r_mid_pzpm"],
    ["l_apex_pzpl", "urethra", "r_mid_pzpm", "l_sv"],
]


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mri_lesion_factory():
    def mri_lesion(number: int) -> dict:
        return {
            "is_index": True,
            "locations": locations[number],
            "size": 40,
            "adc": 700,
            "score": "5",
            "upgraded": "NO",
        }

    return mri_lesion


@pytest.fixture
def mri_form_factory():
    def mri_entry(patient_id: str, lesions: list) -> dict:
        return {
            "patient_id": patient_id,
            "mri_date": "2020-04-01",
            "psa_level": 15,
            "lesions": [*lesions],
            "ece": False,
            "svi": "LEFT",
            "comments": "No comments",
        }

    return mri_entry


@pytest.fixture
def psma_lesion_factory():
    def psma_lesion(number: int) -> dict:
        return {
            "is_index": True,
            "locations": locations[number],
            "suv": 100,
        }

    return psma_lesion


@pytest.fixture
def psma_form_factory():
    def psma_form(patient_id: str, lesions: list) -> dict:
        return {
            "patient_id": patient_id,
            "psma_date": "2020-04-01",
            "lesions": [*lesions],
            "comments": "",
        }

    return psma_form


@pytest.fixture
def pathology_lesion_factory():
    def pathology_lesion() -> dict:
        return {
            "is_index": True,
            "positive_core": 3,
            "total_core": 10,
            "greatest_percentage": 34,
            "grade": "ISUP 5",
            "loc_side": "LEFT",
            "loc_zone": "NA",
        }

    return pathology_lesion


@pytest.fixture
def pathology_form_factory():
    def pathology_form(patient_id: str, lesions: list) -> dict:
        return {
            "patient_id": patient_id,
            "procedure_date": "2020-04-01",
            "specimen_type": "BIOPSY",
            "lesions": [*lesions],
            "comments": "",
        }

    return pathology_form


@pytest.fixture
def mri_entry_without_lesions(mri_form_factory):
    return mri_form_factory("ABC001", lesions=[])


@pytest.fixture
def mri_entry_with_one_lesion(mri_lesion_factory, mri_form_factory):
    lesion = mri_lesion_factory(number=1)
    return mri_form_factory("ABC002", lesions=[lesion])


@pytest.fixture
def mri_entry_with_one_lesion_without_location(mri_lesion_factory, mri_form_factory):
    lesion = mri_lesion_factory(number=0)
    return mri_form_factory("ABC002", lesions=[lesion])


def test_mri_form_serializer(mri_entry_without_lesions, mri_entry_with_one_lesion):
    s = MriEntrySerializer(data=mri_entry_without_lesions)
    assert s.is_valid() is True, s.errors

    s = MriEntrySerializer(data=mri_entry_with_one_lesion)
    assert s.is_valid() is True, s.errors
    assert s.save() == MriEntry.objects.first()
    assert MriLesion.objects.count() == 1
    assert Patient.objects.first().patient_id == mri_entry_with_one_lesion["patient_id"]


def test_post_mri_form(
    api_client, mri_entry_without_lesions, mri_entry_with_one_lesion
):
    # A POST request is sent to MRI api
    # Simple MRI Entry form with no lesions
    r = api_client.post(
        reverse("mri-entry"), data=mri_entry_without_lesions, format="json"
    )

    # A new Patient should be created
    assert Patient.objects.count() == 1, r.data
    # A new MRI Entry should be created
    assert MriEntry.objects.count() == 1, r.data
    # No MRI Lesions should be created
    assert MriLesion.objects.count() == 0, r.data

    # Send a second POST request with the same user info
    r = api_client.post(
        reverse("mri-entry"), data=mri_entry_without_lesions, format="json"
    )
    # The patient count should still be one
    assert Patient.objects.count() == 1, r.data
    # A new MRI Entry should be created (2)
    assert MriEntry.objects.count() == 2, r.data
    # No MRI Lesions should be created
    assert MriLesion.objects.count() == 0, r.data

    # Send a third POST request with same user info
    # this time add one lesion
    r = api_client.post(
        reverse("mri-entry"), data=mri_entry_with_one_lesion, format="json",
    )
    # The patient count should now be two
    assert Patient.objects.count() == 2, r.data
    # The MRI Entry count should now be three
    assert MriEntry.objects.count() == 3, r.data
    # One new MRI Lesions should be created
    assert MriLesion.objects.count() == 1, mri_entry_with_one_lesion
    assert PiradLocation.objects.count() == 1


def test_post_mri_form_edge_cases(
    api_client, mri_entry_with_one_lesion_without_location
):
    r = api_client.post(
        reverse("mri-entry"),
        data=mri_entry_with_one_lesion_without_location,
        format="json",
    )
    # The patient count should now be two
    assert Patient.objects.count() == 1, r.data
    # The MRI Entry count should now be three
    assert MriEntry.objects.count() == 1, r.data
    # One new MRI Lesions should be created
    assert MriLesion.objects.count() == 1, r.data
    # There should not be any locations
    assert PiradLocation.objects.count() == 0, r.data


def test_psma_entry_serializer(psma_form_factory, psma_lesion_factory):
    entry = psma_form_factory("ABC001", lesions=[])
    s = PsmaEntrySerializer(data=entry)
    assert s.is_valid() is True, s.errors
    s.save()

    lesion1 = psma_lesion_factory(number=0)
    entry = psma_form_factory("ABC002", lesions=[lesion1])
    s = PsmaEntrySerializer(data=entry)
    assert s.is_valid() is True, s.errors
    s.save()

    lesion2 = psma_lesion_factory(number=4)
    entry = psma_form_factory("ABC003", lesions=[lesion1, lesion2])
    s = PsmaEntrySerializer(data=entry)
    assert s.is_valid() is True, s.errors
    s.save()

    assert PsmaEntry.objects.count() == 3
    assert PsmaLesion.objects.count() == 3
    assert PiradLocation.objects.count() == 4


def test_post_psma_entry(api_client, psma_form_factory, psma_lesion_factory):
    lesion = psma_lesion_factory(number=0)
    entry = psma_form_factory("ABC001", lesions=[lesion])
    api_client.post(reverse("psma-entry"), data=entry, format="json")
    # Always a new entry
    assert Patient.objects.count() == 1
    assert PsmaEntry.objects.count() == 1, entry
    assert PsmaLesion.objects.count() == 1, entry
    assert PiradLocation.objects.count() == 0, entry


def test_pathology_entry_serializer(pathology_form_factory, pathology_lesion_factory):
    entry = pathology_form_factory("ABC001", lesions=[])
    s = PathologyEntrySerializer(data=entry)
    assert s.is_valid() is True, s.errors
    s.save()

    lesion1 = pathology_lesion_factory()
    entry = pathology_form_factory("ABC002", lesions=[lesion1])
    s = PathologyEntrySerializer(data=entry)
    assert s.is_valid() is True, s.errors
    s.save()

    lesion2 = pathology_lesion_factory()
    entry = pathology_form_factory("ABC003", lesions=[lesion1, lesion2])
    s = PathologyEntrySerializer(data=entry)
    assert s.is_valid() is True, s.errors
    s.save()

    assert Patient.objects.count() == 3
    assert PathologyEntry.objects.count() == 3
    assert PathologyLesion.objects.count() == 3
    assert PiradLocation.objects.count() == 0


def test_post_pathology_entry(
    api_client, pathology_form_factory, pathology_lesion_factory
):
    lesion = pathology_lesion_factory()
    entry = pathology_form_factory("ABC001", lesions=[lesion])
    r= api_client.post(reverse("pathology-entry"), data=entry, format="json")
    # Always a new entry
    assert Patient.objects.count() == 1, r.data
    assert PathologyEntry.objects.count() == 1, entry
    assert PathologyLesion.objects.count() == 1, entry
    assert PiradLocation.objects.count() == 0, entry
