from django import forms
from django.contrib.auth import get_user_model, authenticate

from applications.billing.models import GuestBillingProfile

User = get_user_model()


class BillingEmailForm(forms.ModelForm):
    class Meta:
        model = GuestBillingProfile
        fields = ('email',)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))

    def clean_username(self):
        qs = User.objects.filter(username=self.cleaned_data.get('username'))
        if qs.exists() and qs.count() == 1:
            return self.cleaned_data.get('username')
        raise forms.ValidationError('User with such username doesn\'t exist')

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user:
            return self.cleaned_data
        raise forms.ValidationError('Username or password is not valid')


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists() and qs.count() == 1:
            raise forms.ValidationError('Username already taken')
        return username

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
