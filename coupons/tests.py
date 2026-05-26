from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Coupon
from products.models import Product, Category
from cart.models import Cart, CartItem

User = get_user_model()


class CouponTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='buyer@test.com', name='Buyer', password='TestPass123!'
        )
        self.seller = User.objects.create_user(
            email='seller@test.com', name='Seller', password='TestPass123!', is_seller=True
        )
        self.category = Category.objects.create(name='Clothes')
        self.product = Product.objects.create(
            seller=self.seller, category=self.category,
            name='T-Shirt', description='Cool shirt', price=1000, stock=50
        )
        self.client.force_authenticate(user=self.user)
        self.client.post('/api/cart/add/', {'product_id': self.product.pk, 'quantity': 1})

    def test_expired_coupon_is_rejected(self):
        coupon = Coupon.objects.create(
            code='EXPIRED10',
            discount_type='percentage',
            discount_value=10,
            usage_limit=10,
            times_used=0,
            expiry_date=timezone.now() - timedelta(days=1),  # expired yesterday
            is_active=True,
        )
        response = self.client.post('/api/orders/checkout/', {
            'shipping_address': 'KTM',
            'coupon_code': 'EXPIRED10',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exhausted_coupon_is_rejected(self):
        coupon = Coupon.objects.create(
            code='USED10',
            discount_type='percentage',
            discount_value=10,
            usage_limit=1,
            times_used=1,  # already used up
            expiry_date=timezone.now() + timedelta(days=7),
            is_active=True,
        )
        response = self.client.post('/api/orders/checkout/', {
            'shipping_address': 'KTM',
            'coupon_code': 'USED10',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)