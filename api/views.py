from rest_framework.generics import ListCreateAPIView

from .models import MriEntry, PsmaEntry, PathologyEntry
from .serializers import (
    MriEntrySerializer,
    PsmaEntrySerializer,
    PathologyEntrySerializer,
)


class MriEntryListCreateAPIView(ListCreateAPIView):
    queryset = MriEntry.objects.all()
    serializer_class = MriEntrySerializer


class PsmaEntryListCreateAPIView(ListCreateAPIView):
    queryset = PsmaEntry.objects.all()
    serializer_class = PsmaEntrySerializer


class PathologyEntryListCreateAPIView(ListCreateAPIView):
    queryset = PathologyEntry.objects.all()
    serializer_class = PathologyEntrySerializer
