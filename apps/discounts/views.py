from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Discount, OrderTieredDiscount
from .serializers import DiscountSerializer, OrderTieredDiscountSerializer


class DiscountListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all discounts"""
        discounts = Discount.objects.all().order_by('-priority')
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new discount"""
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Discount.objects.get(pk=pk)
        except Discount.DoesNotExist:
            return None

    def get(self, request, pk):
        discount = self.get_object(pk)
        if not discount:
            return Response({'detail': 'Discount not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)

    def put(self, request, pk):
        discount = self.get_object(pk)
        if not discount:
            return Response({'detail': 'Discount not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiscountSerializer(discount, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        discount = self.get_object(pk)
        if not discount:
            return Response({'detail': 'Discount not found.'}, status=status.HTTP_404_NOT_FOUND)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActiveDiscountsByTypeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, discount_type):
        """List all active discounts filtered by discount_type"""
        valid_types = ['percentage', 'fixed', 'tiered']
        if discount_type not in valid_types:
            return Response({"error": "Invalid discount type."}, status=400)

        discounts = Discount.objects.filter(discount_type=discount_type, is_active=True)
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)
