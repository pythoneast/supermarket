from django.shortcuts import render, redirect
from django.urls import reverse

from applications.accounts.forms import LoginForm, BillingEmailForm
from applications.accounts.models import GuestEmail
from applications.billing.models import BillingProfile
from applications.cart.models import Cart
from applications.orders.models import Order


def checkout_page(request):
    cart, is_new = Cart.objects.get_or_new(request)
    order_obj = None

    if is_new or cart.products.count() == 0:
        return redirect(reverse('cart:cart-page'))

    user = request.user
    billing_profile = None
    guest_user_id = request.session.get('guest_email_id')
    login_form = LoginForm()
    email_form = BillingEmailForm()
    email_action_url = reverse('guest-email-view')

    if user.is_authenticated:
        billing_profile, is_new = BillingProfile.objects.get_or_create(
            user=user, email=user.email)

    elif guest_user_id:
        guest_email_obj = GuestEmail.objects.filter(id=guest_user_id).first()
        if guest_email_obj:
            billing_profile = BillingProfile.objects.create(
                email=guest_email_obj.email)
    else:
        pass

    if billing_profile:
        order_obj = Order.objects.get_or_new(billing_profile, cart)
    return render(request, 'orders/checkout.html', locals())

