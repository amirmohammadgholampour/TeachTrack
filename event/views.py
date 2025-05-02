"""
Event API
=========
This module provides CRUD (Create, Read, Update, Delete) operations for managing events in the system.
The API includes the following endpoints:
1. GET `/event/` - Retrieve a list of events with optional filters.
2. POST `/event/create/` - Create a new event (admin-only).
3. PUT `/event/<event_id>/update/` - Update an existing event (admin-only).
4. DELETE `/event/<event_id>/delete/` - Delete an event (admin-only).

Key Features:
- Staff users (admins) can manage all events.
- Non-staff users can only view events.
- Filtering options for date, time, status, capacity, and future events.
- Pagination for efficient data retrieval.
- Swagger documentation for API endpoints.
"""

from event.models import Event
from event.serializers import EventSerializer
from rest_framework.decorators import api_view
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date
from event.permissions import validate_event, check_event_is_exist

# API endpoint to retrieve a list of events
@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "date",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Enter a date of event"
        ),
        openapi.Parameter(
            "time",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Enter a time of event"
        ),
        openapi.Parameter(
            "status",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Enter the status of the event (held, not_held, in_progress)"
        ),
        openapi.Parameter(
            "capacity",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Enter the capacity of the event (completed, empty)"
        ),
        openapi.Parameter(
            "future_event",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter future events (true/false)"
        ),
        openapi.Parameter(
            "search",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Search events by name"
        )
    ]
)
@api_view(["GET"])
@authenticated_required
def eventGetView(request, *args, **kwargs):
    """
    Retrieves a list of events.
    - Filters can be applied using query parameters (e.g., date, time, status, capacity, future events).
    - Pagination is applied with a default page size of 10.
    """
    queryset = Event.objects.all()

    # Apply filters from query parameters
    filters = {
        "date": request.query_params.get("date"),
        "time": request.query_params.get("time"),
        "status": request.query_params.get("status"),
        "capacity": request.query_params.get("capacity")
    }
    filters = {k: v for k, v in filters.items() if v}
    queryset = queryset.filter(**filters)

    # Apply search filter
    search_query = request.query_params.get("search")
    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    # Filter future events
    future_event = request.query_params.get("future_event")
    if future_event and future_event.lower() == "true":
        user_date = date.today()
        queryset = queryset.filter(date__gte=user_date)

    # Paginate the results
    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = EventSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)

# API endpoint to create a new event
@swagger_auto_schema(
    method="post",
    request_body=EventSerializer,
    responses={
        201: EventSerializer,
        400: "Invalid data",
        401: "Authenticated required",
        403: "Forbidden"
    }
)
@api_view(["POST"])
@authenticated_required
@validate_event
@admin_required
def eventPostView(request, *args, **kwargs):
    """
    Creates a new event (admin-only).
    - Validates the provided data to ensure it meets the required criteria.
    - Returns the created event data on success.
    - If the data is invalid, an error message is returned.
    """
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "Event created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to update an existing event
@swagger_auto_schema(
    method="put",
    request_body=EventSerializer,
    responses={
        200: EventSerializer,
        400: "Invalid data",
        401: "Authenticated required",
        403: "Forbidden",
        404: "Not found"
    }
)
@api_view(["PUT"])
@authenticated_required
@validate_event
@check_event_is_exist
@admin_required
def eventPutView(request, *args, **kwargs):
    """
    Updates an existing event (admin-only).
    - Retrieves the event by ID.
    - Updates the event with the provided data.
    - Returns the updated event data on success.
    - If the data is invalid, an error message is returned.
    """
    event = kwargs.get("event")
    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "Event updated successfully!", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to delete an event
@swagger_auto_schema(
    method="delete",
    responses={
        204: "Deleted successfully!",
        403: "Forbidden",
        404: "Not found"
    }
)
@api_view(["DELETE"])
@authenticated_required
@admin_required
@check_event_is_exist
def eventDeleteView(request, *args, **kwargs):
    """
    Deletes an event (admin-only).
    - Retrieves the event by ID.
    - Deletes the event if it exists.
    - Returns a success message upon successful deletion.
    """
    event = kwargs.get("event")
    event.delete()
    return Response(
        {"detail": "Event deleted successfully!"},
        status=status.HTTP_204_NO_CONTENT
    )