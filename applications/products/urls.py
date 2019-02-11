from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('cbv/', views.ProductList.as_view(), name='product-list-cbv'),
    path('cbv/<str:slug>/', views.ProductSlugDetail.as_view(), name='product-slug-detail-cbv'),
    path('<int:id>/', views.product_detail, name='product-detail'),
    path('<int:pk>/cbv/', views.ProductDetail.as_view(), name='product-detail-cbv'),
    path('create/', views.create_product, name='create_product'),
    path('create_product/', views.create_product_test, name='create_product_test'),
    path('update/<int:id>/', views.update_product, name='update_product'),
    path('update_product/<int:id>/', views.update_product_test, name='update_product_test'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('delete_product/<int:id>/', views.delete_product_test, name='delete_product_test'),
]
