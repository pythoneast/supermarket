import threading
import multiprocessing
import time

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _

from applications.accounts.forms import LoginForm, BillingEmailForm
from applications.accounts.models import GuestEmail
from applications.addresses.forms import AddressForm
from applications.addresses.models import Address
from applications.billing.models import BillingProfile
from applications.cart.models import Cart
from applications.orders.models import Order
from applications.postman.tasks import send_user_email_task


def multi_run_wrapper(args):
   return send_user_email(*args)

def send_user_email(title, message, email=None):
    send_mail(
        title,
        message,
        email,
        ['eldosnursultan@gmail.com',
         'akylova.erkaiym@gmail.com',
         'aliaskar.isakov@gmail.com',
         'aktan.r.a@gmail.com',
         'alymbekovdastan1@gmail.com',
         'dinstamaly@gmail.com',],
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
            title = _("Order successfully completed!")
            message = "Здравствуйте, Эркайым! Ваш заказ успешно оформлен. В течение 15 минут с Вами свяжется наш менеджер! Спасибо за покупку"
            start = time.time()

            # celery 0.001636
            send_user_email_task.delay(title, message)

            # Многопоточность 0.0006
            # my_thread = threading.Thread(target=send_user_email, args=(title, message))
            # my_thread.start()

            # Мультипроцессинг 2.7
            # pool = multiprocessing.Pool(1)
            # pool.map(multi_run_wrapper, [(title, message),])

            # Без асинхронности 2.2
            # send_user_email(title, message, email=None)
            end = time.time()
            delta = end - start
            print(f'Timing: {delta}')
            return redirect('success-page')
        errors.append('Заказ не может быть оформлен!')
    return render(request, 'orders/checkout.html', locals())


def success_page_view(request):
    return render(request, 'orders/success.html', locals())