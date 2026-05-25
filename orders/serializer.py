from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import Cart

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id','product', 'product_name','quantity', 'subtotal' ]

    def get_subtotal(self, obj):
        return obj.get_subtotal()
    

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id','status', 'items', 'total_price', 
            'discount_amount','final_price',
            'shipping_address', 'coupon_code', 
            'created_at', 'updated_at']
        read_only_fields = ['created_at', 'status','total_price', 'discount_amount']

    def get_final_price(self, obj):
        return obj.get_final_price()
    
class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        user = self.context['request'].user
        try:
            cart = user.cart
        except Exception:
            raise serializers.ValidationError('Cart not found for user')
        if cart.items.count() == 0:
            raise serializers.ValidationError('Cart is empty')
        return data