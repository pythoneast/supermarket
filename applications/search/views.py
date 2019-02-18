from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from applications.products.models import Product


class SearchView(ListView):
    model = Product
    template_name = 'products/list-cbv.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        query = request.GET.get('q')
        print(query)
        # exact iexact contains icontains

        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct().order_by('-id')
        print(products)
        paginator = Paginator(products, 10)
        page = self.request.GET.get('page')
        context['object_list'] = paginator.get_page(page)
        # context['data'] = [1, 345, 'hello']
        return context