from itertools import islice
from time import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from applications.categories.models import Category


class Command(BaseCommand):
    help = 'Generates product categories'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Category generating was successfully started at {timezone.localtime(timezone.now())}'))
        start = time()

        Category.objects.bulk_create([
            Category(title='Овощи', slug='vegetables'),
            Category(title='Фрукты', slug='fruits'),
            Category(title='Молочные продукты', slug='diary'),
            Category(title='Напитки', slug='drinks'),
            Category(title='Мясные изделия', slug='meat'),
            Category(title='Полуфабрикаты', slug='polufabrikaty'),
            Category(title='Мучные изделия', slug='bakery'),
        ])

        # categories = ['Овощи', 'Фрукты', 'Молочные продукты',
        #               'Напитки', 'Мясные изделия', 'Полуфабрикаты',
        #               'Мучные изделия']
        # for x in categories:
        #     Category.objects.create(title=x)

        end = time()
        self.stdout.write(self.style.SUCCESS(f'Category generating was successfully finished at {timezone.localtime(timezone.now())}'))
        self.stdout.write(self.style.SUCCESS(f'Timing: {end-start} seconds'))
