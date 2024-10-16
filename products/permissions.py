from rest_framework.permissions import BasePermission

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to only allow authenticated users to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in ['GET']:  # Allow GET requests for everyone
            return True
        return request.user.is_authenticated 