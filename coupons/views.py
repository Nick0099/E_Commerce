from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CouponValidateSerializer


class ValidateCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon   = serializer.validated_data['coupon']
        discount = serializer.validated_data['discount']
        return Response({
            'code':           coupon.code,
            'discount_type':  coupon.discount_type,
            'discount_value': coupon.discount_value,
            'discount_amount': discount,
        })