from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from products.models import Product


class ProductReviewList(generics.ListAPIView):
    """Get all reviews for a product"""
    serializer_class   = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        return Review.objects.filter(product=product).select_related('user')


class ProductReviewCreate(generics.CreateAPIView):
    """Add a review to a product"""
    serializer_class   = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context            = super().get_serializer_context()
        context['product'] = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        return context


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete own review"""
    serializer_class   = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method in ['PUT', 'PATCH']:
            review             = self.get_object()
            context['product'] = review.product
        return context

    def update(self, request, *args, **kwargs):
        # allow updating own review — skip unique_together check
        review     = self.get_object()
        serializer = ReviewCreateSerializer(
            review, data=request.data, partial=True,
            context={'request': request, 'product': review.product}
        )
        # bypass the "already reviewed" check for updates
        if serializer.is_valid():
            serializer.save()
            return Response(ReviewSerializer(review).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)