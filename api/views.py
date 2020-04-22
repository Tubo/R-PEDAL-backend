from rest_framework.generics import ListCreateAPIView

from .models import MriEntry
from .serializers import MriEntrySerializer


class MriEntryListCreateAPIView(ListCreateAPIView):
    queryset = MriEntry.objects.all()
    serializer_class = MriEntrySerializer
