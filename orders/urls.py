from django.urls import path
from . import views

urlpatterns = [
    path('',            views.OrderListView.as_view(),   name='order_list'),
    path('checkout/',   views.CheckoutView.as_view(),    name='checkout'),
    path('<int:pk>/',   views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/cancel/', views.CancelOrderView.as_view(), name='cancel_order'),
]