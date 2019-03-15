from django.contrib import admin

from applications.accounts.models import GuestEmail
from applications.billing.models import BillingProfile


class BillingProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(BillingProfile, BillingProfileAdmin)

class GuestEmailAdmin(admin.ModelAdmin):
    pass

admin.site.register(GuestEmail, GuestEmailAdmin)
