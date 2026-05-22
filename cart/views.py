from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import (
    CartSerializer, AddToCartSerializer,
    UpdateCartItemSerializer, CartItemSerializer
)
from products.models import Product


def get_or_create_cart(user):
    """Get existing cart or create one for the user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """View cart"""
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def delete(self, request):
        """Clear entire cart"""
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'}, status=status.HTTP_204_NO_CONTENT)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Add product to cart or increase quantity if already in cart"""
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product  = Product.objects.get(id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']
        cart     = get_or_create_cart(request.user)

        # check requested quantity doesn't exceed stock
        if quantity > product.stock:
            return Response(
                {'error': f'Only {product.stock} items available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # product already in cart — add to existing quantity
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                return Response(
                    {'error': f'Only {product.stock} items available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        """Update quantity of a cart item"""
        cart     = get_or_create_cart(request.user)
        item     = get_object_or_404(CartItem, pk=pk, cart=cart)
        serializer = UpdateCartItemSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)

        # check stock
        if serializer.validated_data['quantity'] > item.product.stock:
            return Response(
                {'error': f'Only {item.product.stock} items available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        """Remove item from cart"""
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        item.delete()
        return Response({'message': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)