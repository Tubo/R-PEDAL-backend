from rest_framework.generics import ListCreateAPIView

from .models import Entry
from .serializers import EntrySerializer


class EntryListCreateAPIView(ListCreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
