from django.db import models

# user ---> 1 billing profile
# guest ---> 100000000 guest billing profile

class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email