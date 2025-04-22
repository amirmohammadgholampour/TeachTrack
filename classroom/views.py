"""
This module provides API views for managing classrooms.

Views:
    - classroomGetView: Retrieve a list of classrooms with optional filters.
    - classroomPostView: Create a new classroom (admin-only).
    - classroomPutView: Update an existing classroom (admin-only).
    - classroomDeleteView: Delete a classroom (admin-only).

Decorators:
    - @authenticated_required: Ensures the user is authenticated.
    - @admin_required: Ensures the user has admin privileges.

Pagination:
    - PageNumberPagination is used to paginate the classroom list.
"""

from classroom.models import ClassRoom
from classroom.serializers import ClassRoomSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi 
from rest_framework.pagination import PageNumberPagination
from common.is_admin import admin_required
from common.is_authenticated import authenticated_required

@swagger_auto_schema(
    method="get",
    operation_summary="Get class room list",
    manual_parameters=[
        openapi.Parameter("name", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Name of class room"),
        openapi.Parameter("student", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Student Name"),
        openapi.Parameter("teacher", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Teacher Name"),
        openapi.Parameter("base", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Base Name"),
        openapi.Parameter("field", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Field Name"),
    ]
)
@api_view(["GET"])
@authenticated_required
def classroomGetView(request, *args, **kwargs):
    """
    Retrieve a list of classrooms.

    - Filters can be applied using query parameters (e.g., name, student, teacher, base, field).
    - Pagination is applied with a default page size of 10.
    """
    user = request.user 
    
    # Filter classrooms based on user type (staff or student)
    queryset = ClassRoom.objects.filter(students=user) if not user.is_staff else ClassRoom.objects.all()

    # Apply filters from query parameters
    filters = {
        "base__icontains": request.query_params.get("base"),
        "field__icontains": request.query_params.get("field"),
        "name__icontains": request.query_params.get("name"),
        "students__username__icontains": request.query_params.get("student"),
        "teachers__username__icontains": request.query_params.get("teacher"),
    }
    filters = {k: v for k, v in filters.items() if v} 
    queryset = queryset.filter(**filters)

    # Paginate the queryset
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = ClassRoomSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)

@swagger_auto_schema(
        method="post",
        operation_summary="Create a class room", 
        request_body=ClassRoomSerializer,
        responses={
            201: ClassRoomSerializer(),
            400: "Bad request",
            401: "UnAuthenticated",
            403: "Forbidden"
        }
)
@api_view(["POST"])
@admin_required
@authenticated_required
def classroomPostView(request):
    """
    Create a new classroom (admin-only).

    - Validates the 'base' field to ensure it is between 10 and 12.
    - Returns the created classroom data on success.
    """
    base = request.data.get("base")
    if not 10 <= base <= 12:
        return Response(
            {"detail":"The base should 10th or 11th or 12th"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ClassRoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"ClassRoom created successfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

@swagger_auto_schema(
    method="put",
    operation_summary="Update a class room",
    request_body=ClassRoomSerializer,
    responses={
        200: "Updated successfully!",
        400: "Bad request",
        401: "UnAuthenticated",
        403: "Forbidden",
        404: "Not found"
    }
)
@api_view(["PUT"])
@admin_required
@authenticated_required
def classroomPutView(request, *args, **kwargs):
    """
    Update an existing classroom (admin-only).

    - Retrieves the classroom by ID.
    - Validates the 'base' field to ensure it is between 10 and 12.
    - Updates the classroom with the provided data.
    """
    classroom_id = kwargs.get("classroom_id")
    try:
        classroom = ClassRoom.objects.get(id=classroom_id)
    except ClassRoom.DoesNotExist:
        return Response(
            {"detail":"ClassRoom not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    base = request.data.get("base")
    try:
        base = int(base)
        if not 10 <= base <= 12:
            return Response(
                {"detail":"The base should 10th or 11th or 12th"},
                status=status.HTTP_400_BAD_REQUEST
            )
    except (ValueError, TypeError):
        return Response(
            {"detail": "The base must be a valid Integer"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ClassRoomSerializer(classroom, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"ClassRoom updated successfully!", "data":serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

@swagger_auto_schema(
    method="delete",
    operation_summary="Delete a classroom",
    request_body=ClassRoomSerializer,
    responses={
        204: "Deleted successfully!",
        403: "Forbidden",
        404: "Not found",
    }
)
@api_view(["DELETE"])
@admin_required
@authenticated_required
def classroomDeleteView(request, *args, **kwargs):
    """
    Delete a classroom (admin-only).

    - Retrieves the classroom by ID.
    - Deletes the classroom if it exists.
    """
    classroom_id = kwargs.get("classroom_id")
    try:
        classroom = ClassRoom.objects.get(id=classroom_id)
    except ClassRoom.DoesNotExist:
        return Response(
            {"detail":"ClassRoom not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    classroom.delete()
    return Response(
        {"detail":"ClassRoom deleted successfully!"},
        status=status.HTTP_204_NO_CONTENT
    )