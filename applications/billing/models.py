from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save


User = get_user_model()


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        has_user = 'user' if self.user else 'guest'
        return f'{self.email} {has_user}'


def post_save_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.create(user=instance, email=instance.email)

post_save.connect(
    post_save_user_profile,
    sender=User
)


