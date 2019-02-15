from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse

from applications.categories.models import Category
from applications.products.models import Product
from .forms import ContactsForm, LoginForm, RegistrationForm

User = get_user_model()


def main_page(request):
    categories = Category.objects.all()
    products_list = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'index.html', locals())


def contacts(request):
    contacts_form = ContactsForm(request.POST or None)
    if request.method == 'POST':
        data = request.POST
        print(data)
        print(data.get('csrfmiddlewaretoken'))
        print(data.get('name'))
        print(data.get('email'))
        if 'gmail.com' not in data.get('email'):
            print('Only gmail accounts')
    return render(request, 'contacts.html', locals())


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('main-page'))

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
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


def learn_bootstrap(request):
    return render(request, 'bootstrap-learn.html', locals())
