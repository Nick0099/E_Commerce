from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    user_name  = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model  = Review
        fields = ['id', 'user', 'user_name', 'product', 'rating',
                  'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'product', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ['rating', 'comment']

    def validate(self, data):
        request = self.context['request']
        product = self.context['product']

        # check user hasn't already reviewed this product
        if Review.objects.filter(user=request.user, product=product).exists():
            raise serializers.ValidationError('You have already reviewed this product')
        return data

    def create(self, validated_data):
        return Review.objects.create(
            user    = self.context['request'].user,
            product = self.context['product'],
            **validated_data
        )