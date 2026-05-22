from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review
from products.models import Product


def update_product_rating(product):
    """Recalculate and store average rating on the product"""
    avg = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    # we'll add avg_rating field to Product in a moment
    Product.objects.filter(pk=product.pk).update(avg_rating=round(avg, 1) if avg else 0)


@receiver(post_save, sender=Review)
def review_saved(sender, instance, **kwargs):
    update_product_rating(instance.product)


@receiver(post_delete, sender=Review)
def review_deleted(sender, instance, **kwargs):
    update_product_rating(instance.product)