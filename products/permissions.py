from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSellerOrReadOnly(BasePermission):

    def has_permission(self, request, view):          # no obj here
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_seller

    def has_object_permission(self, request, view, obj):   # obj only here
        if request.method in SAFE_METHODS:
            return True
        return obj.seller == request.user