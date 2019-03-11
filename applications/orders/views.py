from django.shortcuts import render, redirect
from django.urls import reverse

from applications.cart.models import Cart
from applications.orders.models import Order


def checkout_page(request):
    if not request.user.is_authenticated:
        return redirect(f'/login/?next=/cart/checkout/')

    cart, is_new = Cart.objects.get_or_new(request)
    order, is_new = Order.objects.get_or_create(cart=cart)
    return render(request, 'orders/checkout.html', locals())

