from django.db import models
from django.db.models.signals import pre_save, post_save

from applications.billing.models import BillingProfile
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


class OrderManager(models.Manager):
    def get_or_new(self, billing_profile, cart):
        new = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile, cart=cart, active=True)
        if qs.count() == 1:
            order_obj = qs.first()
        else:
            order_obj = Order.objects.create(
                billing_profile=billing_profile,
                cart=cart)
            new = True
        return order_obj

class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.CharField(max_length=100, unique=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='created')
    shipment_total = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipment_total = self.shipment_total
        order_total = cart_total + shipment_total
        self.total = order_total
        self.save()
        return order_total

def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id(instance)


pre_save.connect(pre_save_order_id_receiver, sender=Order)


def pre_save_update_old_orders(sender, instance, *args, **kwargs):
    old_order_qs = Order.objects.exclude(
        billing_profile=instance.billing_profile).filter(
        cart=instance.cart, active=True)
    if old_order_qs.exists():
        old_order_qs.update(active=False)


pre_save.connect(pre_save_update_old_orders, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order = qs.first()
            order.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
