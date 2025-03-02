from rest_framework import serializers
from .models import Item, ItemAmount, Check, CheckItems


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["pk", "title", "price"]


class CheckSerializer(serializers.ModelSerializer):
    createdTime = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    class Meta:
        model = Check
        fields = ["pk", "file_path", "total_price", "timestamp"]


class CheckItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckItems
        fields = ["check_id", "item"]