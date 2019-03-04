import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse

from supermarket.utils import unique_slug_generator

from applications.categories.models import Category


class InStockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(in_stock=False)

    def search(self, query):
        return self.get_queryset().filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(tags__title__icontains=query)
        ).distinct().order_by('-id')

    def get_by_slug_name(self, slug):
        return self.get_queryset().get(slug=slug)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3934343433)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'product_images/{new_filename}/{final_filename}'


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True, db_index=True)
    slug = models.SlugField(blank=True, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    objects = models.Manager()
    instock = InStockManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product-slug-detail-cbv', kwargs={'slug': self.slug})


class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_image_path)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.product.title}.jpg'


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    instance.in_stock = False if instance.quantity == 0 else True


# def product_post_delete_receiver(sender, instance, *args, **kwargs):
#     Product.objects.all().delete()


pre_save.connect(product_pre_save_receiver, sender=Product)
# post_delete.connect(product_post_delete_receiver, sender=Product)
