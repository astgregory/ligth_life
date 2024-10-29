from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminReadOnly(BasePermission):
    """
    Разрешение, позволяющее администраторам читать все записи, а изменять только свои записи,
    а обычным пользователям - читать и изменять только свои объекты.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff and request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
