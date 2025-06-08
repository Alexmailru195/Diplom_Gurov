from rest_framework import serializers
from .models import PointOfSale


class PointOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSale
        fields = '__all__'
