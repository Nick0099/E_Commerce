from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product, Category
from .models import Order

User = get_user_model()


class OrderTest(TestCase):

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
        # add item to cart
        self.client.post('/api/cart/add/', {'product_id': self.product.pk, 'quantity': 2})

    def test_checkout_creates_order(self):
        response = self.client.post('/api/orders/checkout/', {
            'shipping_address': 'Kathmandu, Nepal'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)

    def test_checkout_reduces_stock(self):
        self.client.post('/api/orders/checkout/', {
            'shipping_address': 'Kathmandu, Nepal'
        })
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 48)

    def test_checkout_clears_cart(self):
        self.client.post('/api/orders/checkout/', {
            'shipping_address': 'Kathmandu, Nepal'
        })
        response = self.client.get('/api/cart/')
        self.assertEqual(response.data['item_count'], 0)

    def test_checkout_empty_cart_fails(self):
        self.client.delete('/api/cart/')
        response = self.client.post('/api/orders/checkout/', {
            'shipping_address': 'Kathmandu, Nepal'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_order(self):
        self.client.post('/api/orders/checkout/', {'shipping_address': 'KTM'})
        order    = Order.objects.get(user=self.user)
        response = self.client.post(f'/api/orders/{order.pk}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')

    def test_cancel_restores_stock(self):
        self.client.post('/api/orders/checkout/', {'shipping_address': 'KTM'})
        order = Order.objects.get(user=self.user)
        self.client.post(f'/api/orders/{order.pk}/cancel/')
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 50)

    def test_order_list_shows_own_orders_only(self):
        self.client.post('/api/orders/checkout/', {'shipping_address': 'KTM'})
        other_user = User.objects.create_user(
            email='other@test.com', name='Other', password='TestPass123!'
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.get('/api/orders/')
        self.assertEqual(len(response.data['results']), 0)