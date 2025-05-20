from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('api/products/', views.ProductListCreateAPI.as_view(), name='api_product_list_create'),
    path('api/products/<int:pk>/', views.ProductDetailAPI.as_view(), name='api_product_detail'),
]
