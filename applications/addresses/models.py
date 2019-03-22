from django.db import models

from applications.billing.models import BillingProfile


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, related_name='addresses', on_delete=models.SET_NULL, blank=True, null=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=6)

    @property
    def get_address_display(self):
        return f'{self.country} {self.city} {self.street}, {self.apartment} {self.postal_code}'

    def __str__(self):
        return self.country
