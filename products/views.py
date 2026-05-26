from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Category
from .serializers import ProductSerializer,ProductCreateSerializer, CategorySerializer
from .permissions import IsSellerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductList(generics.ListAPIView):
    queryset           = Product.objects.filter(is_active=True).select_related('seller', 'category')
    serializer_class   = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['category', 'seller']
    search_fields      = ['name', 'description', 'category__name']
    ordering_fields    = ['price', 'created_at', 'name']

class ProductCreate(generics.CreateAPIView):
    serializer_class   = ProductCreateSerializer
    permission_classes = [IsSellerOrReadOnly]

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Product.objects.filter(is_active=True).select_related('seller', 'category')
    permission_classes = [IsSellerOrReadOnly]    

    def get_serializer_class(self):
     if self.request.method in ['PUT', 'PATCH']:
         return ProductCreateSerializer
     return ProductSerializer
     
class MyProductList(generics.ListAPIView):
    """Seller sees only their own products"""
    serializer_class   = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)