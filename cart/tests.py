from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product, Category
from .models import Cart, CartItem

User = get_user_model()


class CartTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@test.com', name='User', password='TestPass123!'
        )
        self.seller = User.objects.create_user(
            email='seller@test.com', name='Seller', password='TestPass123!', is_seller=True
        )
        self.category = Category.objects.create(name='Food')
        self.product = Product.objects.create(
            seller=self.seller, category=self.category,
            name='Rice', description='Good rice', price=500, stock=100
        )
        self.client.force_authenticate(user=self.user)

    def test_cart_created_automatically(self):
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        response = self.client.post('/api/cart/add/', {
            'product_id': self.product.pk,
            'quantity': 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 2)

    def test_add_same_product_increases_quantity(self):
        self.client.post('/api/cart/add/', {'product_id': self.product.pk, 'quantity': 2})
        self.client.post('/api/cart/add/', {'product_id': self.product.pk, 'quantity': 3})
        cart = Cart.objects.get(user=self.user)
        item = cart.items.get(product=self.product)
        self.assertEqual(item.quantity, 5)

    def test_cannot_add_more_than_stock(self):
        response = self.client.post('/api/cart/add/', {
            'product_id': self.product.pk,
            'quantity': 999
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_total_is_correct(self):
        self.client.post('/api/cart/add/', {'product_id': self.product.pk, 'quantity': 2})
        response = self.client.get('/api/cart/')
        self.assertEqual(float(response.data['total']), 1000.0)

    def test_clear_cart(self):
        self.client.post('/api/cart/add/', {'product_id': self.product.pk, 'quantity': 1})
        response = self.client.delete('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_cannot_access_cart(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)