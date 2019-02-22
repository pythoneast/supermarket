from django.contrib import admin

from applications.tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)

