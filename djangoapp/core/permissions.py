from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied

#check user is authenticated
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return True
        raise AuthenticationFailed('Authentication credentials not provided')
    
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an admin (superuser)
        return request.user and request.user.is_superuser
