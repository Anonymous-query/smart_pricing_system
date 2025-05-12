from django.urls import path
from .views import (
    DiscountListCreateAPIView,
    DiscountDetailAPIView,
    ActiveDiscountsByTypeAPIView,
)

urlpatterns = [
    path('api/v1/discounts/', DiscountListCreateAPIView.as_view(), name='discount-list-create'),
    path('api/v1/discounts/<int:pk>/', DiscountDetailAPIView.as_view(), name='discount-detail'),
    path('api/v1/discounts/type/<str:discount_type>/', ActiveDiscountsByTypeAPIView.as_view(), name='active-discounts-by-type'),
]
