from rest_framework import generics
from .serializers import ItemSerializer, CheckSerializer, CheckItemsSerializer
from .models import Item, ItemAmount, Check, CheckItems
from rest_framework.exceptions import NotFound, ValidationError


class CheckView(generics.RetrieveAPIView):
    serializer_class = CheckSerializer
    lookup_field = 'pk'

    def get_object(self):
        pass


class CheckCreationView(generics.CreateAPIView):
    serializer_class = CheckSerializer


    def perform_create(self, serializer):
        pass
