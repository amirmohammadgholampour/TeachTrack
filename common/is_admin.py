"""
This module provides a decorator to enforce admin-level access control for API views.

Decorators:
    - admin_required: Ensures that the requesting user has an admin user type or is staff.

Usage:
    Apply the `@admin_required` decorator to any API view to restrict access to admin users only.

Example:
    @api_view(["POST"])
    @admin_required
    def some_admin_view(request):
        # Your view logic here
        return Response({"detail": "Success"}, status=status.HTTP_200_OK)
"""
from functools import wraps 
from rest_framework.response import Response 
from rest_framework import status 

def admin_required(view_func):
    @wraps(view_func)
    def _wraps_view(request, *args, **kwargs):
        user = request.user 
        if (not user.is_authenticated) or (user.user_type != "admin"):
            return Response(
                {"detail":"You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)
    return _wraps_view