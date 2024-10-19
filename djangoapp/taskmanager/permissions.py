from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed

#check user is admin or owner
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True 
        if request.user.is_authenticated:
            return True
        raise AuthenticationFailed('Authentication credentials not provided')
    



    
