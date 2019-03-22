from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

from applications.accounts.models import GuestEmail


User = get_user_model()


class BillingModelManager(models.Manager):
    def get_or_new(self, request):
        is_new = False
        obj = None
        user = request.user
        guest_user_id = request.session.get('guest_email_id')
        if user.is_authenticated:
            obj, is_new = self.model.objects.get_or_create(
                user=user, email=user.email)

        elif guest_user_id:
            guest_email_obj = GuestEmail.objects.filter(id=guest_user_id).first()
            if guest_email_obj:
                obj, is_new = self.model.objects.get_or_create(
                    guest=guest_email_obj,
                    email=guest_email_obj.email)
        else:
            pass
        return obj, is_new


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    guest = models.OneToOneField(GuestEmail, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BillingModelManager()

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


