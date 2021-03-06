from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Delivery, Order
from .serializers import OrderSerializer, DeliverySerializer, MyOrderSerializer
from product.models import Cart
from product.serializers import CartSerializer, ProductSerializer


class OrderAPIView(APIView):

    def get(self, request):
        cart_obj = Cart.objects.get_or_new(request)[0]
        cart_serializer = CartSerializer(cart_obj)
        print(cart_obj.products)
        delivery = Delivery.objects.all()
        serializer = DeliverySerializer(delivery, many=True)
        return Response({'delivery': serializer.data,
                         'cart': cart_serializer.data})

    def post(self, request):
        cart_obj = Cart.objects.get_or_new(request)[0]
        user = request.user
        try:
            order = Order.objects.create(
                cart=cart_obj,
                user=user)
        except:
            raise ValidationError("Заказ уже сделан")
        return Response(status=status.HTTP_201_CREATED)

    def get_object(self):
        return self.request.user


class MyOrderAPIView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.filter(user=request.user)
        except TypeError:
            return Response({'error': 'У вас нет заказов',
                             'user': f'{request.user}'},
                            status=status.HTTP_200_OK)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
