import random
import os

from django.db import models


class InStockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(in_stock=False)


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
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True, db_index=True)

    objects = models.Manager()
    instock = InStockManager()

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_image_path)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.product.title}.jpg'
