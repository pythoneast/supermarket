from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import is_safe_url

from applications.accounts.forms import LoginForm, RegistrationForm, BillingEmailForm
from applications.billing.models import GuestBillingProfile

User = get_user_model()


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('main-page'))

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if redirect_path and is_safe_url(redirect_path, request.get_host()):
                return redirect(str(redirect_path))
            else:
                return redirect(reverse('main-page'))
        else:
            return redirect(reverse('login-page'))
    return render(request, 'account/login.html', locals())


def logout_page(request):
    logout(request)
    return redirect(reverse('main-page'))


def register_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('main-page'))

    form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                            email=form.cleaned_data.get('email'),
                                            password=form.cleaned_data.get('password'))
            print(user)
            login(request, user)
            return redirect(reverse('main-page'))
    return render(request, 'account/register.html', locals())


def guest_email_view(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    form = BillingEmailForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data.get('email')
        guest_email_obj = form.save()
        request.session['guest_email_id'] = guest_email_obj.id
        if redirect_path and is_safe_url(redirect_path, request.get_host()):
            return redirect(str(redirect_path))
        else:
            return redirect(reverse('main-page'))
    return render(request, 'account/login.html', locals())
