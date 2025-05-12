from django.urls import path
from .views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    ProductPriceAPIView,
)

urlpatterns = [
    path('api/v1/products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('api/v1/products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/v1/products/<int:pk>/price/', ProductPriceAPIView.as_view(), name='product-price'),
]
