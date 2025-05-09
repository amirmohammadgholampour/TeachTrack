"""
Present/Absent API
==================
This module provides CRUD (Create, Read, Update, Delete) operations for managing attendance records in the system.
The API includes the following endpoints:
1. GET `/attendance/` - Retrieve a list of attendance records with optional filters.
2. POST `/attendance/create/` - Create a new attendance record.
3. PUT `/attendance/<attendance_id>/update/` - Update an existing attendance record.
4. DELETE `/attendance/<attendance_id>/delete/` - Delete an attendance record.

Key Features:
- Staff users (admins) can manage all attendance records.
- Non-staff users can only view their own attendance records.
- Filtering options for user, status, classroom, and date.
- Pagination for efficient data retrieval.
- Swagger documentation for API endpoints.
"""

from present_absent.models import PresentAbsent 
from present_absent.serializers import PresentAbsentSerializer
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from rest_framework.decorators import api_view
from present_absent.permissions import attending_validations, check_attending_exist
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status 

# API endpoint to retrieve a list of attendance records
@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "user",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter by username"
        ),
        openapi.Parameter(
            "status",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter by attendance status (present/absent)"
        ),
        openapi.Parameter(
            "classroom",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter by classroom name"
        ),
        openapi.Parameter(
            "date",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter by attendance date (YYYY-MM-DD)"
        ),
        openapi.Parameter(
            "search",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Search by username"
        )
    ]
)
@api_view(["GET"])
@authenticated_required
def getAttendingView(request, *args, **kwargs):
    """
    Retrieves a list of attendance records.
    - Non-staff users can only view their own attendance records.
    - Staff users (admins) can view all attendance records.
    - Filters can be applied using query parameters (e.g., user, status, classroom, date).
    - Search functionality is available for usernames.
    - Pagination is applied with a default page size of 10.
    """
    req_user = request.user 
    queryset = PresentAbsent.objects.filter(user=req_user) if req_user.user_type != "admin" else PresentAbsent.objects.all() 
    filters = {
        "user__username": request.query_params.get("user"),
        "status": request.query_params.get("status"),
        "classroom__name": request.query_params.get("classroom"),
        "date": request.query_params.get("date")
    }
    filters = {k:v for k,v in filters.items() if v}
    queryset = queryset.filter(**filters)

    search_query = request.query_params.get("search")
    if search_query:
        queryset = queryset.filter(user__username=search_query)

    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = PresentAbsentSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)

# API endpoint to create a new attendance record
@swagger_auto_schema(
    method="post",
    request_body=PresentAbsentSerializer
)
@api_view(["POST"])
@authenticated_required
@attending_validations
def postAttendingView(request):
    """
    Creates a new attendance record.
    - Validates the provided data to ensure it meets the required criteria.
    - Returns the created attendance record data on success.
    - If the data is invalid, an error message is returned.
    """
    serializer = PresentAbsentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Attending created successfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
# API endpoint to update an existing attendance record
@swagger_auto_schema(
    method="put",
    request_body=PresentAbsentSerializer
)
@api_view(["PUT"])
@authenticated_required
@check_attending_exist
@attending_validations
def putAttendingView(request, *args, **kwargs):
    """
    Updates an existing attendance record.
    - Retrieves the attendance record by ID.
    - Updates the attendance record with the provided data.
    - Returns the updated attendance record data on success.
    - If the data is invalid, an error message is returned.
    """
    attending = kwargs.get("attending")
    serializer = PresentAbsentSerializer(attending, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Attending updated successfully!", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to delete an attendance record
@swagger_auto_schema(
    method="delete"
)
@api_view(["DELETE"])
@authenticated_required
@check_attending_exist
@admin_required
def deleteAttendingView(request, *args, **kwargs):
    """
    Deletes an attendance record.
    - Retrieves the attendance record by ID.
    - Deletes the attendance record if it exists.
    - Returns a success message upon successful deletion.
    """
    attending = kwargs.get("attending")
    attending.delete()
    return Response(
        {"detail":"Attending deleted successfully!"},
        status=status.HTTP_204_NO_CONTENT
    )