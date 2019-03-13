from django.contrib import admin

from applications.billing.models import BillingProfile, GuestBillingProfile


class BillingProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(BillingProfile, BillingProfileAdmin)

class GuestBillingProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(GuestBillingProfile, GuestBillingProfileAdmin)
