from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product

User = get_user_model()


class Review(models.Model):
    user       = models.ForeignKey(User,    on_delete=models.CASCADE, related_name='reviews')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating     = models.PositiveIntegerField(
                    validators=[MinValueValidator(1), MaxValueValidator(5)]
                 )
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} — {self.product.name} ({self.rating}★)"

    class Meta:
        unique_together = ['user', 'product']   # one review per user per product
        ordering        = ['-created_at']