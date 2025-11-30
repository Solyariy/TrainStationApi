from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.is_staff:
            return True
        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        return False
