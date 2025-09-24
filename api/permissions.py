from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow owners to access/modify their objects; allow admins full access.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, "role") and request.user.role == "admin":
            return True
        return obj.owner == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(request.user, "role", None) == "admin"
