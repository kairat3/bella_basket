from django.contrib import admin

# Register your models here.
from cart.models import Order, Delivery
from product.models import Cart

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Delivery)
