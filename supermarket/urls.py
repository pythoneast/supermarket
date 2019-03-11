from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from applications.accounts.views import (
    login_page,
    logout_page,
    register_page,
)
from .views import (
    main_page,
    contacts,
    learn_bootstrap,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main-page'),
    path('api/', include('applications.api.urls')),
    path('products/', include('applications.products.urls')),
    path('search/', include('applications.search.urls')),
    path('cart/', include('applications.cart.urls')),
    path('contacts/', contacts, name='contacts'),
    path('login/', login_page, name='login-page'),
    path('logout/', logout_page, name='logout-page'),
    path('register/', register_page, name='register-page'),
    path('learn_bs/', learn_bootstrap, name='learn-bootstrap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
