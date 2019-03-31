from django import forms
from django.contrib.auth import get_user_model, authenticate

from applications.accounts.models import GuestEmail

User = get_user_model()


class BillingEmailForm(forms.ModelForm):
    class Meta:
        model = GuestEmail
        fields = ('email',)


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))

    def clean_email(self):
        qs = User.objects.filter(email=self.cleaned_data.get('email'))
        if qs.exists() and qs.count() == 1:
            return self.cleaned_data.get('email')
        raise forms.ValidationError('User with such email doesn\'t exist')

    def clean(self):
        user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if user:
            return self.cleaned_data
        raise forms.ValidationError('Email or password is not valid')


class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists() and qs.count() == 1:
            raise forms.ValidationError('Email already taken')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords must match')
        return password2
