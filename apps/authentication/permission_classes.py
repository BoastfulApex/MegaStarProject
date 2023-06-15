from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


class IsAuthenticatedCustom(BasePermission):
    """
    Custom permission class to check if a user is authenticated.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi ro\'yxatdan o\'tmagan', code=401)
        return True
