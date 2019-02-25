from django.contrib.auth import get_user_model
from django.db import models

from applications.products.models import Product

User = get_user_model()


class CartManager(models.Manager):
    def get_or_new(self, request):
        new = False
        cart_id = request.session.get('cart_id', None)  # get data from session
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            if request.user.is_authenticated and not cart_obj.user:
                cart_obj.user = request.user
                cart_obj.save()
            print('Cart object has been founded')
        else:
            cart_obj = self.new(user=request.user)
            new = True
            request.session['cart_id'] = cart_obj.id
            print('Cart has been created')
        return cart_obj, new

    def new(self, user=None):
        user_obj = None
        if user and user.is_authenticated:
            user_obj = user
        return self.model.objects.create(user=user_obj)


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
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=OPENED)

    objects = CartManager()

    def __str__(self):
        return str(self.id)
