from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from applications.accounts.views import (
    login_page,
    logout_page,
    register_page,
    guest_email_view,
)
from .views import (
    main_page,
    contacts,
    learn_bootstrap,
)

from applications.orders.views import success_page_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main-page'),
    path('api/', include('applications.api.urls')),
    path('products/', include('applications.products.urls')),
    path('search/', include('applications.search.urls')),
    path('cart/', include('applications.cart.urls')),
    path('addresses/', include('applications.addresses.urls')),
    path('contacts/', contacts, name='contacts'),
    path('login/', login_page, name='login-page'),
    path('logout/', logout_page, name='logout-page'),
    path('register/', register_page, name='register-page'),
    path('register/email/', guest_email_view, name='guest-email-view'),
    path('learn_bs/', learn_bootstrap, name='learn-bootstrap'),
    path('success_page/', success_page_view, name='success-page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
