from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSellerOrReadOnly(BasePermission):
    """
    Custom permission to only allow sellers of a product to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_seleer

    def has_permission(self, request, view,obj):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)