"""
Event Permissions
=================
This module provides custom permission decorators to validate and manage event-related operations.
The decorators ensure that the requests meet specific criteria before proceeding to the corresponding views.

Key Features:
1. `validate_event` - Validates the event creation request to ensure:
   - The event's date and time do not conflict with existing events.
   - The event is not being created for a past date.
2. `check_event_is_exist` - Ensures that the event exists in the database before performing operations like update or delete.

Usage:
- These decorators are applied to view functions to enforce the required validation and permission checks.
"""

from functools import wraps
from datetime import datetime, date
from event.models import Event
from rest_framework.response import Response
from rest_framework import status

def validate_event(view_func):
    """
    Decorator to validate event creation requests.
    - Ensures that the event's date and time do not conflict with existing events.
    - Prevents creating events for past dates.

    Args:
        view_func (function): The view function to wrap.

    Returns:
        function: The wrapped view function with validation logic.
    """
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        # Parse the requested event date and time from the request data
        req_date = datetime.strptime(request.data.get("date"), "%Y-%m-%d").date()
        req_time = datetime.strptime(request.data.get("time"), "%H:%M").time()

        # Check if an event already exists with the same date and time
        main_date = Event.objects.filter(date=req_date, time=req_time)
        if main_date.exists():
            return Response(
                {"detail": "This date and time already exist for event"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the event is not being created for a past date
        str_req_date = datetime.strptime(request.data.get("date"), "%Y-%m-%d").date()
        date_now = date.today()
        if date_now > str_req_date:
            return Response(
                {"detail": "You are not allowed to create events for past dates"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Proceed to the view function if validation passes
        return view_func(request, *args, **kwargs)
    return _wrap_view


def check_event_is_exist(func):
    """
    Decorator to check if an event exists in the database.
    - Retrieves the event by its ID from the URL parameters.
    - If the event does not exist, returns a 404 response.

    Args:
        func (function): The view function to wrap.

    Returns:
        function: The wrapped view function with existence check logic.
    """
    @wraps(func)
    def _wrap_view(request, *args, **kwargs):
        # Retrieve the event ID from the URL parameters
        event_id = kwargs.get("event_id")
        try:
            # Attempt to fetch the event from the database
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            # Return a 404 response if the event does not exist
            return Response(
                {"detail": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Add the event object to the kwargs for use in the view function
        kwargs["event"] = event
        return func(request, *args, **kwargs)
    return _wrap_view