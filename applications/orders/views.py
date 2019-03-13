from django.shortcuts import render, redirect
from django.urls import reverse

from applications.accounts.forms import LoginForm, BillingEmailForm
from applications.billing.models import BillingProfile, GuestBillingProfile
from applications.cart.models import Cart
from applications.orders.models import Order


def checkout_page(request):
    # if not request.user.is_authenticated:
    #     return redirect(f'/login/?next=/cart/checkout/')
    cart, is_new = Cart.objects.get_or_new(request)
    order, is_new = Order.objects.get_or_create(cart=cart)

    guest_user_id = request.session.get('guest_email_id')

    if request.user.is_authenticated:
        billing_profile = BillingProfile.objects.get_or_create(user=request.user)
    elif guest_user_id:
        billing_profile = GuestBillingProfile.objects.get(id=guest_user_id)
    else:
        pass
    login_form = LoginForm()
    email_form = BillingEmailForm()
    email_action_url = reverse('guest-billing')
    return render(request, 'orders/checkout.html', locals())

