from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView

urlpatterns = [
    path('api/v1/orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('api/v1/orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
