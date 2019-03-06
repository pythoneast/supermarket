from django.forms import inlineformset_factory

from applications.categories.models import Category
from applications.products.forms import ProductForm, ProductImageForm
from applications.products.models import ProductImage, Product


def categories_context(request):
    ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)
    form = ProductForm()
    return {
        "formset": ProductImageFormSet(),
        "form": form,
        "categories_list": Category.objects.all(),
    }
