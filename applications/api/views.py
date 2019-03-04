from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from applications.products.models import Product


def products_list(request):
    data = []
    products = Product.instock.all()
    for product in products:
        product_data = {
            'title': product.title,
            'description': product.description,
            'price': product.price,
        }
        data.append(product_data)
    return JsonResponse(data, safe=False)
