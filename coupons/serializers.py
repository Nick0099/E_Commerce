from rest_framework import serializers
from .models import Coupon


class CouponValidateSerializer(serializers.Serializer):
    code       = serializers.CharField()
    order_total = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        try:
            coupon = Coupon.objects.get(code=data['code'])
        except Coupon.DoesNotExist:
            raise serializers.ValidationError({'code': 'Coupon not found'})

        if not coupon.is_valid():
            raise serializers.ValidationError({'code': 'Coupon is expired or inactive'})

        if data['order_total'] < coupon.min_order:
            raise serializers.ValidationError(
                {'code': f'Minimum order of Rs.{coupon.min_order} required'}
            )

        data['coupon']    = coupon
        data['discount']  = coupon.get_discount(data['order_total'])
        return data