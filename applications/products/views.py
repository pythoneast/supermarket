from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.forms import inlineformset_factory

from applications.cart.models import Cart
from applications.products.forms import ProductForm, ProductImageForm, ProductTestForm
from applications.products.models import Product, ProductImage


class ProductList(ListView):
    # queryset = Product.instock.all()
    # queryset = Product.objects.all()
    model = Product
    template_name = 'products/list-cbv.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.instock.all().order_by('-id')
        paginator = Paginator(products, 4)
        page = self.request.GET.get('page')
        context['object_list'] = paginator.get_page(page)
        # context['data'] = [1, 345, 'hello']
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/detail-cbv.html'


class ProductSlugDetail(DetailView):
    model = Product
    template_name = 'products/detail-slug-cbv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        cart_obj, is_new = Cart.objects.get_or_new(request)
        context['cart_obj'] = cart_obj
        return context

def product_list(request):
    products = Product.instock.all().order_by('-id')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    data = [1, 'asfs', 435.3]
    return render(request, 'products/list.html', locals())


def product_detail(request, id):
    product = get_object_or_404(Product, id=id, in_stock=True)
    return render(request, 'products/detail.html', locals())


def create_product(request):
    form = ProductForm(request.POST or None)
    title = 'Create a product'
    ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
            formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
            if formset.is_valid():
                formset.save()
            return redirect(product.get_absolute_url())
    formset = ProductImageFormSet()
    return render(request, 'products/create_product.html', locals())


def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=product)
    title = 'Update a product'
    ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
            formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
            if formset.is_valid():
                formset.save()
            return redirect(product.get_absolute_url())
    formset = ProductImageFormSet(instance=product)
    return render(request, 'products/update_product.html', locals())


@require_POST
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('products:product-list-cbv')


def create_product_test(request):
    form = ProductTestForm(request.POST or None)
    ProductImageTestFormset = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)

    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
            formset = ProductImageTestFormset(request.POST, request.FILES, instance=product)
            if formset.is_valid():
                formset.save()
                formset.save()
            return redirect(product.get_absolute_url())
    formset = ProductImageTestFormset()
    return render(request, 'products/create_product_test.html', locals())


def update_product_test(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductTestForm(request.POST or None, instance=product)

    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
            return redirect(product.get_absolute_url())
    return render(request, 'products/update_product_test.html', locals())


@require_POST
def delete_product_test(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect(reverse('products:product-list-cbv'))
