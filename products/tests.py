from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Category

User = get_user_model()


class ProductModelTest(TestCase):

    def setUp(self):
        self.seller = User.objects.create_user(
            email='seller@test.com', name='Seller', password='TestPass123!', is_seller=True
        )
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            seller      = self.seller,
            category    = self.category,
            name        = 'Laptop',
            description = 'A good laptop',
            price       = 50000,
            stock       = 10,
        )

    def test_product_created(self):
        self.assertEqual(self.product.name, 'Laptop')
        self.assertEqual(self.product.stock, 10)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Laptop')

    def test_product_is_in_stock(self):
        self.assertTrue(self.product.is_in_stock())

    def test_product_out_of_stock(self):
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock())

    def test_category_product_count(self):
        self.assertEqual(self.category.products.count(), 1)


class ProductAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.seller = User.objects.create_user(
            email='seller@test.com', name='Seller', password='TestPass123!', is_seller=True
        )
        self.buyer = User.objects.create_user(
            email='buyer@test.com', name='Buyer', password='TestPass123!'
        )
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            seller=self.seller, category=self.category,
            name='Phone', description='A phone', price=20000, stock=5
        )

    def test_anyone_can_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anyone_can_view_product_detail(self):
        response = self.client.get(f'/api/products/{self.product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_seller_cannot_create_product(self):
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post('/api/products/create/', {
            'name': 'Test', 'description': 'Test',
            'price': 100, 'stock': 5, 'category': self.category.pk
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_can_create_product(self):
        self.client.force_authenticate(user=self.seller)
        response = self.client.post('/api/products/create/', {
            'name': 'New Product', 'description': 'Desc',
            'price': 1000, 'stock': 3, 'category': self.category.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_products(self):
        response = self.client.get('/api/products/?search=Phone')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)