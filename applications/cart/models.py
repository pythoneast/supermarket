from django.contrib.auth import get_user_model
from django.db import models

from applications.products.models import Product

User = get_user_model()


class Cart(models.Model):
    OPENED = 'op'
    CLOSED = 'cl'
    STATUS_CHOICES = (
        (OPENED, 'Opened'),
        (CLOSED, 'Closed'),
    )
    user = models.ForeignKey(User, blank=True, null=True, related_name='carts', on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product, blank=True, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=OPENED)

    def __str__(self):
        return str(self.user.id)
