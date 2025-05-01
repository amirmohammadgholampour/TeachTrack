"""
Report Card API
===============
This module provides CRUD (Create, Read, Update, Delete) operations for managing report cards in the system.
The API includes the following endpoints:
1. GET `/reportcards/` - Retrieve a list of report cards with optional filters.
2. POST `/reportcards/create/` - Create a new report card (admin-only).
3. PUT `/reportcards/<reportcard_id>/update/` - Update an existing report card (admin-only).
4. DELETE `/reportcards/<reportcard_id>/delete/` - Delete a report card (admin-only).

Key Features:
- Staff users (admins) can manage all report cards.
- Non-staff users can only view their own report cards.
- Filtering options for classroom and disciplinary status.
- Pagination for efficient data retrieval.
- Swagger documentation for API endpoints.
"""

from reportcard.models import ReportCard 
from reportcard.serializers import ReportCardSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from reportcard.permissions import validate_user_and_scores, check_reportcard_exists

# API endpoint to retrieve a list of report cards
@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "class_room",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Enter classroom of student"
        ),
        openapi.Parameter(
            "disciplinary_status",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Enter a disciplinary status of student (very good, good, normal, bad, very bad)"
        )
    ]
)
@api_view(["GET"])
@authenticated_required
def reportcardGetView(request, *args, **kwargs):
    """
    Retrieves a list of report cards.
    - Non-staff users can only view their own report cards.
    - Staff users (admins) can view all report cards.
    - Filters can be applied using query parameters (e.g., classroom, disciplinary status).
    - Pagination is applied with a default page size of 10.
    """
    user = request.user 
    if (not user.is_staff) or (user.user_type != "admin"):
        queryset = ReportCard.objects.filter(user=user)
    else:
        queryset = ReportCard.objects.all()

    try:    
        filters = {
            "class_room_id": request.query_params.get("classroom"),
            "disciplinary_status__exact": request.query_params.get("disciplinary_status")
        }
        filters = {k: v for k, v in filters.items() if v} 
        queryset = queryset.filter(**filters)
    except ValueError:
        return Response(
            {"detail":"Invalid data"},
            status=status.HTTP_400_BAD_REQUEST
        )   
    
    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = ReportCardSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)

# API endpoint to create a new report card
@swagger_auto_schema(
    method="post",
    request_body=ReportCardSerializer,
    responses={
        201: ReportCardSerializer,
        401: "Authenticated required",
        400: "Invalid data",
        403: "Forbidden",
    }
)
@api_view(["POST"])
@authenticated_required
@validate_user_and_scores
@admin_required
def reportcardPostView(request):
    """
    Creates a new report card (admin-only).
    - Validates the provided data to ensure it meets the required criteria.
    - Returns the created report card data on success.
    - If the data is invalid, an error message is returned.
    """
    serializer = ReportCardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Report Card created successfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to update an existing report card
@swagger_auto_schema(
    method="put",
    request_body=ReportCardSerializer
)
@api_view(["PUT"])
@authenticated_required
@validate_user_and_scores
@admin_required
@check_reportcard_exists
def reportcardPutView(request, *args, **kwargs):
    """
    Updates an existing report card (admin-only).
    - Retrieves the report card by ID.
    - Updates the report card with the provided data.
    - Returns the updated report card data on success.
    - If the data is invalid, an error message is returned.
    """
    reportcard = kwargs.get("reportcard")
    
    serializer = ReportCardSerializer(reportcard, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"ReportCard updated successfully!", "data":serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to delete a report card
@swagger_auto_schema(
    method="delete",
    responses={
        204: "Deleted successfully!",
        403: "Forbidden",
        404: "Not found",
    }
)
@api_view(["DELETE"])
@authenticated_required
@admin_required
@check_reportcard_exists
def reportcardDeleteView(request, *args, **kwargs):
    """
    Deletes a report card (admin-only).
    - Retrieves the report card by ID.
    - Deletes the report card if it exists.
    - Returns a success message upon successful deletion.
    """
    reportcard = kwargs.get("reportcard")
    reportcard.delete()
    return Response(
        {"detail":"ReportCard deleted successfully!"},
        status=status.HTTP_204_NO_CONTENT
    )