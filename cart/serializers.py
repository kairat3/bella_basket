import random
from rest_framework import serializers

from .models import Delivery, Order
from product.models import Cart
from product.serializers import CartSerializer


STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
)


class DeliverySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)


class OrderSerializer(serializers.Serializer):
    order_id = serializers.CharField(max_length=100, required=False)
    cart = serializers.IntegerField()
    status = serializers.CharField(default='created')
    address = serializers.CharField(max_length=255)
    shipment_total = serializers.DecimalField(max_digits=100,
                                              decimal_places=2, required=False)
    delivery = serializers.IntegerField()

    def create(self, validated_data):
        cart = Cart.objects.get(pk=validated_data['cart'])
        delivery = Delivery.objects.get(pk=validated_data['delivery'])
        shipment_total = cart.subtotal + delivery.price
        status = validated_data['status']
        address = validated_data['address']
        list_numbers = [x for x in range(1, 9999999)]
        order_id = random.choice(list_numbers)
        order = Order.objects.create(
            order_id=order_id,
            cart=cart,
            delivery=delivery,
            status=status,
            address=address,
            shipment_total=shipment_total,
            user=cart.user
        )
        return order


class MyOrderSerializer(serializers.Serializer):
    order_id = serializers.CharField(max_length=100)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    address = serializers.CharField(max_length=255)
    shipment_total = serializers.DecimalField(max_digits=100, decimal_places=2)
    delivery = serializers.CharField(max_length=255)
    cart = CartSerializer()
