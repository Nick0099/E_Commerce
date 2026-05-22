from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal       = serializers.SerializerMethodField()

    class Meta:
        model  = CartItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'subtotal', 'added_at']
        read_only_fields = ['added_at']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class CartSerializer(serializers.ModelSerializer):
    items       = CartItemSerializer(many=True, read_only=True)
    total       = serializers.SerializerMethodField()
    item_count  = serializers.SerializerMethodField()

    class Meta:
        model  = Cart
        fields = ['id', 'items', 'total', 'item_count', 'updated_at']

    def get_total(self, obj):
        return obj.get_total()

    def get_item_count(self, obj):
        return obj.get_item_count()


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity   = serializers.IntegerField(min_value=1, default=1)

    def validate_product_id(self, value):
        from products.models import Product
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product not found or inactive')
        if not product.is_in_stock():
            raise serializers.ValidationError('Product is out of stock')
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CartItem
        fields = ['quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Quantity must be at least 1')
        return value
    