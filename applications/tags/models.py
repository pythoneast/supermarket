from django.db import models
from django.db.models.signals import pre_save

from applications.products.models import Product
from supermarket.utils import unique_slug_generator


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.TextField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, related_name='tags', blank=True)

    def __str__(self):
        return self.title


def tags_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tags_pre_save_receiver, sender=Tag)
