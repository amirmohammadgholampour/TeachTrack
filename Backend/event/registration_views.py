"""
Registration API
=================
This module provides CRUD (Create, Read, Update, Delete) operations for managing event registrations.
The API includes the following endpoints:
1. GET `/registration/` - Retrieve a list of registrations with optional filters.
2. POST `/registration/create/` - Create a new registration.
3. PUT `/registration/<registration_id>/update/` - Update an existing registration (admin-only).
4. DELETE `/registration/<registration_id>/delete/` - Delete a registration.

Key Features:
- Admin users can manage all registrations.
- Non-admin users can only view and manage their own registrations.
- Filtering options for event, user, status, and date-based filters (future, past, today).
- Pagination for efficient data retrieval.
- Swagger documentation for API endpoints.
"""

from event.models import Registration
from event.serializers import RegistrationSerializer
from rest_framework.decorators import api_view
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from event.registration_permissions import validations_registeration, check_registration_exist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from datetime import date

# API endpoint to retrieve a list of registrations
@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "event",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter by event name"
        ),
        openapi.Parameter(
            "user",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Filter by user ID"
        ),
        openapi.Parameter(
            "status",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter by registration status"
        ),
        openapi.Parameter(
            "search",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Search by username or event name"
        )
    ]
)
@api_view(["GET"])
@authenticated_required
def registerGetView(request, *args, **kwargs):
    """
    Retrieves a list of registrations.
    - Filters can be applied using query parameters (e.g., event, user, status, search).
    - Supports date-based filters for future, past, and today's registrations.
    - Pagination is applied with a default page size of 10.
    """
    user = request.user
    # Admin users can view all registrations; others can view their own
    queryset = Registration.objects.filter(id=user.id) if user.user_type != "admin" else Registration.objects.all()

    # Apply search filter
    search = request.query_params.get("search")
    if search:
        queryset = queryset.filter(
            Q(user__username__icontains=search) |
            Q(event__name__icontains=search)
        )

    # Apply additional filters
    filters = {
        "event__name": request.query_params.get("event"),
        "user": request.query_params.get("user"),
        "event__status": request.query_params.get("status")
    }
    filters = {k: v for k, v in filters.items() if v}
    queryset = queryset.filter(**filters)

    # Filter future events
    future_event = request.query_params.get("future")
    if future_event and future_event.lower() == "true":
        user_date = date.today()
        queryset = queryset.filter(event__date__gte=user_date)

    # Filter past events
    past_event = request.query_params.get("past")
    if past_event and past_event.lower() == "true":
        user_date = date.today()
        queryset = queryset.filter(event__date__lte=user_date)

    # Filter today's registrations
    today_register = request.query_params.get("today_register")
    if today_register and today_register.lower() == "true":
        user_date = date.today()
        queryset = queryset.filter(register_at=user_date)

    # Apply ordering
    ordering = request.query_params.get("ordering")
    allowed_fields = ["register_at", "-register_at"]
    if ordering in allowed_fields:
        queryset = queryset.order_by(ordering)

    # Paginate the results
    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = RegistrationSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)

# API endpoint to create a new registration
@swagger_auto_schema(
    method="post",
    request_body=RegistrationSerializer
)
@api_view(["POST"])
@authenticated_required
@validations_registeration
def registerPostView(request, *args, **kwargs):
    """
    Creates a new registration.
    - Validates the provided data to ensure it meets the required criteria.
    - Associates the registration with the authenticated user.
    - Returns the created registration data on success.
    """
    req_user = request.user
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=req_user)
        return Response(
            {"detail": "Registered successfully!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to update an existing registration
@swagger_auto_schema(
    method="put",
    request_body=RegistrationSerializer
)
@api_view(["PUT"])
@authenticated_required
@validations_registeration
@admin_required
def registerPutView(request, *args, **kwargs):
    """
    Updates an existing registration (admin-only).
    - Retrieves the registration by ID.
    - Updates the registration with the provided data.
    - Returns the updated registration data on success.
    """
    req_user = request.user

    # Retrieve the registration by ID
    register_id = kwargs.get("registration_id")
    try:
        registration = Registration.objects.get(id=register_id)
    except Registration.DoesNotExist:
        return Response(
            {"detail": "Registration not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Update the registration
    serializer = RegistrationSerializer(registration, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(user=req_user)
        return Response(
            {"detail": "Registration updated successfully!", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to delete a registration
@api_view(["DELETE"])
@authenticated_required
@check_registration_exist
def registerDeleteView(request, *args, **kwargs):
    """
    Deletes a registration.
    - Ensures the authenticated user is authorized to delete the registration.
    - Deletes the registration if it exists and the user is authorized.
    - Returns a success message upon successful deletion.
    """
    req_user = request.user
    registration = kwargs.get("registration")

    # Ensure the user is authorized to delete the registration
    if req_user.id != registration.user.id:
        return Response(
            {"detail": "You are not allowed to delete this registration"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Delete the registration
    registration.delete()
    return Response(
        {"detail": "Registration deleted successfully!"},
        status=status.HTTP_204_NO_CONTENT
    )