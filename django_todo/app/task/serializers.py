from rest_framework import serializers
from ..models.task import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        # fields = '__all__'
        exclude = ('create_time', 'update_time')
