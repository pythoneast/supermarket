from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from applications.products.models import Product


class ProductList(ListView):
    model = Product
    template_name = 'products/list-cbv.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = [1, 345, 'hello']
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/detail-cbv.html'


def product_list(request):
    products = Product.instock.all().order_by('-id')
    data = [1, 'asfs', 435.3]
    return render(request, 'products/list.html', locals())


def product_detail(request, id):
    product = get_object_or_404(Product, id=id, in_stock=True)
    return render(request, 'products/detail.html', locals())
