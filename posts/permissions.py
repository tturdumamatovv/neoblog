from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwnerOrAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or IsAdminUser().has_permission(request, view)


class IsCommentOwnerOrPostAuthorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj.author == request.user or obj.post.author == request.user or
                    IsAdminUser().has_permission(request, view))
        return False
