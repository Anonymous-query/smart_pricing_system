from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from apps.discounts.models import Discount
from apps.products.models import Product
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from apps.orders.services import OrderService

class OrderListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all orders for the authenticated user."""
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new order and calculate its total price."""
        user = request.user
        data = request.data

        items_data = data.get('items', [])
        discounts_data = data.get('discounts', [])

        if not items_data or not isinstance(items_data, list):
            return Response({"error": "Items list is required and must be a list."},
                            status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=user)

        try:
            for item in items_data:
                product_id = item.get('product')
                quantity = item.get('quantity')

                if not product_id or not isinstance(quantity, int) or quantity <= 0:
                    raise ValidationError(f"Invalid product ID or quantity: {item}")
                
                
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    raise ValidationError(f"Product with ID {product_id} does not exist.")

                OrderItem.objects.create(order=order, product=product, quantity=quantity)

            # Assign discounts if provided
            for discount_id in discounts_data:
                try:
                    discount = Discount.objects.get(id=discount_id)
                    order.discounts.add(discount)
                except Discount.DoesNotExist:
                    raise ValidationError(f"Discount with ID {discount_id} does not exist.")

            order_service = OrderService(order)
            total_price = order_service.calculate_total()

            serializer = OrderSerializer(order)
            response_data = serializer.data
            response_data['total_price'] = total_price


            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except ValidationError as ve:
            order.delete()  # Clean up partial data
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            order.delete()
            return Response({"error": "Unexpected error occurred", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Retrieve a specific order with its details."""
        try:
            order = Order.objects.get(id=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)