from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from .views import main_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main-page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
