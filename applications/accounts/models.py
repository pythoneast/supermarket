from django.db import models

# user ---> 1 billing profile
# guest ---> 100000000 guest billing profile

class GuestEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email