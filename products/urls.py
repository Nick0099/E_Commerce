from django.urls import path
from . import views

urlpatterns = [
    path('',              views.ProductList.as_view(),      name='product_list'),
    path('create/',       views.ProductCreate.as_view(),    name='product_create'),
    path('<int:pk>/',     views.ProductDetail.as_view(),    name='product_detail'),
    path('my/',           views.MyProductList.as_view(),    name='my_products'),
    path('categories/',          views.CategoryListCreate.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(),     name='category_detail'),
]