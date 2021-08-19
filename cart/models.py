from django.contrib.auth import get_user_model
from django.db import models

from product.models import Cart


User = get_user_model()


STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
)


class Delivery(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):

    order_id = models.CharField(max_length=100, unique=True, db_index=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES,
        default='created'
    )
    address = models.CharField(max_length=255)

    shipment_total = models.DecimalField(max_digits=100, decimal_places=2,
                                         default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    delivery = models.ForeignKey(
        Delivery, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return str(self.order_id)
