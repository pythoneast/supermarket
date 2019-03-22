from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse

from applications.accounts.forms import LoginForm, BillingEmailForm
from applications.accounts.models import GuestEmail
from applications.addresses.forms import AddressForm
from applications.addresses.models import Address
from applications.billing.models import BillingProfile
from applications.cart.models import Cart
from applications.orders.models import Order


def send_user_email(title, message, email):
    send_mail(
        title,
        message,
        email,
        ['akylova.erkaiym@gmail.com'],
        fail_silently=False,
    )
    return True


def checkout_page(request):
    errors = []
    cart, is_new = Cart.objects.get_or_new(request)
    order_obj = None
    if is_new or cart.products.count() == 0:
        return redirect(reverse('cart:cart-page'))

    login_form = LoginForm()
    email_form = BillingEmailForm()
    address_form = AddressForm()
    address_id = request.session.get('address_id')

    billing_profile, is_new_billing = BillingProfile.objects.get_or_new(request)
    if billing_profile:
        order_obj, is_new_order = Order.objects.get_or_new(billing_profile, cart)
        if address_id:
            address_obj = Address.objects.filter(id=address_id).first()
            if address_obj:
                order_obj.address = address_obj
                order_obj.save(update_fields=['address'])

    if request.method == 'POST':
        can_be_completed = order_obj.can_be_completed()
        if can_be_completed:
            order_obj.complete()
            del request.session['cart_id']
            del request.session['cart_items']
            title = "Успешное оформление заказа"
            message = "Здравствуйте, Эркайым! Ваш заказ успешно оформлен. В течение 15 минут с Вами свяжется наш менеджер! Спасибо за покупку"
            send_user_email(title, message, email=None)
            return redirect('success-page')
        errors.append('Заказ не может быть оформлен!')
    return render(request, 'orders/checkout.html', locals())


def success_page_view(request):
    return render(request, 'orders/success.html', locals())