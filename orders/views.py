from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from cart.models import Cart


class OrderListView(generics.ListAPIView):
    serializer_class   = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class   = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        cart    = request.user.cart
        items   = cart.items.select_related('product').all()

        # validate all items are still in stock
        for item in items:
            if item.quantity > item.product.stock:
                return Response(
                    {'error': f'{item.product.name} only has {item.product.stock} left'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # calculate total
        total = sum(item.get_subtotal() for item in items)

        # apply coupon if provided
        discount      = 0
        coupon_code   = serializer.validated_data.get('coupon_code', '')
        if coupon_code:
            from coupons.models import Coupon
            try:
                coupon   = Coupon.objects.get(code=coupon_code, is_active=True)
                discount = coupon.get_discount(total)
                coupon.times_used += 1
                coupon.save()
            except Exception:
                return Response(
                    {'error': 'Invalid or expired coupon'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # create order
        order = Order.objects.create(
            user             = request.user,
            shipping_address = serializer.validated_data['shipping_address'],
            total_price      = total,
            discount_amount  = discount,
            coupon_code      = coupon_code,
        )

        # create order items + reduce stock
        for item in items:
            OrderItem.objects.create(
                order         = order,
                product       = item.product,
                product_name  = item.product.name,
                product_price = item.product.price,
                quantity      = item.quantity,
            )
            item.product.stock -= item.quantity
            item.product.save()

        # clear cart
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)

        if order.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Only pending or confirmed orders can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # restore stock
        for item in order.items.select_related('product').all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save()

        order.status = 'cancelled'
        order.save()
        return Response({'message': 'Order cancelled successfully'})