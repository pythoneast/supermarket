from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save, m2m_changed

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
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=OPENED)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def cart_total_m2m_receiver(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(
    cart_total_m2m_receiver,
    sender=Cart.products.through
)

def total_price_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal != 0:
        instance.total = instance.subtotal + 100
    else:
        instance.total = 0

pre_save.connect(
    total_price_pre_save_receiver,
    sender=Cart
)
