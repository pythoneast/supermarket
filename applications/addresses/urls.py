from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'address'

urlpatterns = [
    path('create/', views.create_shipping_address, name='create'),
]
