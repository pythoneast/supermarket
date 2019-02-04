from django.contrib import admin

from applications.categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'parent']


admin.site.register(Category, CategoryAdmin)
