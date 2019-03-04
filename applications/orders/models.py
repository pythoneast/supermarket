from django.db import models
from django.db.models.signals import pre_save

from applications.cart.models import Cart
from applications.products.models import Product

from supermarket.utils import unique_order_id

# from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
    ('delivered', 'Delivered'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='created')
    shipment_total = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)

    def __str__(self):
        return self.order_id

def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id(instance)


pre_save.connect(pre_save_order_id_receiver, sender=Order)