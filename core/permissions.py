from rest_framework import permissions

class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name__in=['Admin', 'Moderator']).exists()

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the owner or admins
        return obj.owner == request.user or request.user.groups.filter(name='Admin').exists()
