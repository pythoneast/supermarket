from django.contrib import admin

from applications.products.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


admin.site.register(Product, ProductAdmin)
