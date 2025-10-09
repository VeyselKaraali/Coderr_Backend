from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessUser(BasePermission):
    """
    Permission class that allows access only to authenticated users
    with type 'business'.
    """
    def has_permission(self, request, view):
        """
        Checks if the requesting user is authenticated and is a business user.

        Returns:
            bool: True if user is authenticated and of type 'business', else False.
        """
        user = request.user
        return bool(user and user.is_authenticated and user.type == 'business')


class IsCustomerUser(BasePermission):
    """
    Permission class that allows access only to authenticated users
    with type 'customer'.
    """
    def has_permission(self, request, view):
        """
        Checks if the requesting user is authenticated and is a customer user.

        Returns:
            bool: True if user is authenticated and of type 'customer', else False.
        """
        user = request.user
        return bool(user and user.is_authenticated and user.type == 'customer')


class IsProfileOwnerOrReadOnly(BasePermission):
    """
    Permission class that grants full access to the owner of a profile object,
    but read-only access to others.
    """
    def has_object_permission(self, request, view, obj):
        """
        Allows safe methods (GET, HEAD, OPTIONS) for any user.
        Allows modifications only if the user owns the profile.

        Returns:
            bool: True if safe method or the requesting user owns the profile.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsReviewerOrReadOnly(BasePermission):
    """
    Permission class that grants full access to the reviewer of an object,
    but read-only access to others.
    """
    def has_object_permission(self, request, view, obj):
        """
        Allows safe methods (GET, HEAD, OPTIONS) for any user.
        Allows modifications only if the requesting user is the reviewer.

        Returns:
            bool: True if safe method or the requesting user is the reviewer.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.reviewer == request.user
