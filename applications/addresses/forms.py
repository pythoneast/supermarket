from django import forms

from applications.addresses.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('billing_profile',)
