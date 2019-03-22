from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import is_safe_url

from applications.addresses.forms import AddressForm
from applications.billing.models import BillingProfile


def create_shipping_address(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    form = AddressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        address_obj = form.save(commit=False)
        billing_profile, is_new_billing = BillingProfile.objects.get_or_new(request)
        if billing_profile:
            address_obj.billing_profile = billing_profile
            address_obj.save()
            request.session['address_id'] = address_obj.id
        else:
            return redirect('cart:checkout')

        if redirect_path and is_safe_url(redirect_path, request.get_host()):
            return redirect(str(redirect_path))
        else:
            return redirect(reverse('main-page'))
    return render(request, 'account/login.html', locals())