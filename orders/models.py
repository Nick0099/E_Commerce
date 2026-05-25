from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),     
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),  
    ]
    
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'orders')
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = 'PENDING')
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    shipping_address = models.TextField()
    coupon_code = models.CharField(max_length = 50, blank = True, null = True)
    discount_amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"
    
    def get_final_price(self):
        return self.total_price - self.discount_amount
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'items')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    product_name = models.CharField(max_length = 255)
    quantity = models.PositiveIntegerField(default = 1)
    product_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name} for Order #{self.order.id}"
    
    def get_total_price(self):
        return self.quantity * self.price
    