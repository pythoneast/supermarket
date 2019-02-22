from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from applications.products.models import Product


class SearchView(ListView):
    template_name = 'search/index.html'

    def get_queryset(self):
        request = self.request
        # exact iexact contains icontains
        query = request.GET.get('q') # None
        if query:
            products = Product.instock.search(query)
        else:
            products = Product.instock.none()
        paginator = Paginator(products, 20)
        page = self.request.GET.get('page')
        return paginator.get_page(page)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
