from django.urls import path
from .views import (
    products_list,
)

urlpatterns = [
    path('v1/products', products_list, name='products-list'),
]
