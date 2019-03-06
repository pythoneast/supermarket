from django.shortcuts import render

from applications.cart.models import Cart
from applications.orders.models import Order


def checkout_page(request):
    cart, is_new = Cart.objects.get_or_new(request)
    order, is_new = Order.objects.get_or_create(cart=cart)
    return render(request, 'orders/checkout.html', locals())

