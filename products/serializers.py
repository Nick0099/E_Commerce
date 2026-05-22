from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ['id', 'name', 'description', 'product_count']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductSerializer(serializers.ModelSerializer):
    seller_name   = serializers.CharField(source='seller.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_in_stock   = serializers.SerializerMethodField()

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'image', 'is_active', 'is_in_stock',
            'seller', 'seller_name', 'category', 'category_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']

    def get_is_in_stock(self, obj):
        return obj.is_in_stock()


class ProductCreateSerializer(serializers.ModelSerializer):
    """Separate serializer for creating/updating products"""
    class Meta:
        model  = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category', 'is_active']

    def create(self, validated_data):
        # automatically set seller to logged-in user
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)