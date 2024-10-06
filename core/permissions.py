from rest_framework import permissions

class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Admin', 'Moderator']).exists()