from rest_framework import serializers
from .models import Order
from cart.serializers import CartSerializer


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = '__all__'
