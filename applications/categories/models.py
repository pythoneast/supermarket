from django.db import models
from django.db.models.signals import pre_save

from applications.products.utils import unique_slug_generator


class Category(models.Model):
    title = models.CharField(max_length=255)  # High technology
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(category_pre_save_receiver, sender=Category)
