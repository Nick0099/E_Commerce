from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WishlistItem
from .serializers import WishlistItemSerializer


class WishlistView(generics.ListAPIView):
    serializer_class   = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related('product')


class WishlistToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id required'}, status=status.HTTP_400_BAD_REQUEST)

        item, created = WishlistItem.objects.get_or_create(
            user_id=request.user.id, product_id=product_id
        )

        if not created:
            item.delete()
            return Response({'message': 'Removed from wishlist'})

        return Response({'message': 'Added to wishlist'}, status=status.HTTP_201_CREATED)