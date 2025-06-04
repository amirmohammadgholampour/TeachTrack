"""
This module provides a decorator to enforce authentication for API views.

Decorators:
    - authenticated_required: Ensures that the requesting user is authenticated.

Usage:
    Apply the `@authenticated_required` decorator to any API view to restrict access to authenticated users only.

Example:
    @api_view(["GET"])
    @authenticated_required
    def some_authenticated_view(request):
        # Your view logic here
        return Response({"detail": "Success"}, status=status.HTTP_200_OK)
"""
from functools import wraps 
from rest_framework.response import Response 
from rest_framework import status 

def authenticated_required(view_func):
    @wraps(view_func)
    def _wraps_view(request, *args, **kwargs):
        user = request.user 
        if not user.is_authenticated:
            return Response(
                {"detail":"Authenticated required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)
    return _wraps_view