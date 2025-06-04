"""
Registration Permissions
=========================
This module provides custom permission decorators to validate and manage event registration operations.
The decorators ensure that the requests meet specific criteria before proceeding to the corresponding views.

Key Features:
1. `validations_registeration` - Validates registration requests to ensure:
   - The event is not full (capacity check).
   - The event is open for registration (status check).
   - The user has not exceeded the maximum allowed registrations.
2. `check_registration_exist` - Ensures that the registration exists in the database before performing operations like update or delete.

Usage:
- These decorators are applied to view functions to enforce the required validation and permission checks.
"""

from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from event.models import Registration

def validations_registeration(view_func):
    """
    Decorator to validate registration requests.
    - Ensures that the event is not full (capacity check).
    - Ensures that the event is open for registration (status check).
    - Ensures that the user has not exceeded the maximum allowed registrations.

    Args:
        view_func (function): The view function to wrap.

    Returns:
        function: The wrapped view function with validation logic.
    """
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        # Check if the event is full
        event_capacity = request.data.get("event__capacity")
        if event_capacity == "completed":
            return Response(
                {"detail": "Capacity for this event is full"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if the event is open for registration
        event_status = request.data.get("event__status")
        if event_status in ["held", "in_progress"]:
            return Response(
                {"detail": "This event is not open for registrations"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if the user has exceeded the maximum allowed registrations
        req_user = request.user
        if Registration.objects.filter(user=req_user).count() >= 3:
            return Response(
                {"detail": "You are not allowed to register for more events"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Proceed to the view function if validation passes
        return view_func(request, *args, **kwargs)
    return _wrap_view

def check_registration_exist(view_func):
    """
    Decorator to check if a registration exists in the database.
    - Retrieves the registration by its ID from the URL parameters.
    - If the registration does not exist, returns a 404 response.

    Args:
        view_func (function): The view function to wrap.

    Returns:
        function: The wrapped view function with existence check logic.
    """
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        # Retrieve the registration ID from the URL parameters
        register_id = kwargs.get("registration_id")
        try:
            # Attempt to fetch the registration from the database
            registration = Registration.objects.get(id=register_id)
        except Registration.DoesNotExist:
            # Return a 404 response if the registration does not exist
            return Response(
                {"detail": "Registration not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Add the registration object to the kwargs for use in the view function
        kwargs["registration"] = registration
        return view_func(request, *args, **kwargs)
    return _wrap_view