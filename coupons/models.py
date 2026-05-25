from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed',      'Fixed Amount'),
    ]

    code           = models.CharField(max_length=50, unique=True)
    discount_type  = models.CharField(max_length=20, choices=TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usage_limit    = models.PositiveIntegerField(default=1)
    times_used     = models.PositiveIntegerField(default=0)
    expiry_date    = models.DateTimeField()
    is_active      = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        return (
            self.is_active and
            self.times_used < self.usage_limit and
            self.expiry_date > timezone.now()
        )

    def get_discount(self, total):
        if self.discount_type == 'percentage':
            return round(total * self.discount_value / 100, 2)
        return min(self.discount_value, total)   # fixed — can't discount more than total