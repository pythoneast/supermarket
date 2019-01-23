from django.contrib import admin
from applications.products.models import Product, ProductImage


admin.site.register(Product)
admin.site.register(ProductImage)
