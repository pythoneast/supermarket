from django.urls import path
from .views import product_list, product_detail, ProductList, ProductDetail, ProductSlugDetail

app_name = 'products'
urlpatterns = [
    path('', product_list, name='product-list'),
    path('cbv/', ProductList.as_view(), name='product-list-cbv'),
    path('cbv/<str:slug>/', ProductSlugDetail.as_view(), name='product-slug-detail-cbv'),
    path('<int:id>', product_detail, name='product-detail'),
    path('<int:pk>/cbv/', ProductDetail.as_view(), name='product-detail-cbv'),
]
