from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart-page'),
    path('update/', views.cart_update, name='update'),
]
