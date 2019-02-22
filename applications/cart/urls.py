from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart-page'),
]
