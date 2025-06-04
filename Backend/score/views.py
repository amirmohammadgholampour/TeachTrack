# Importing necessary modules and components for handling models, serializers, authentication, responses, pagination, and API documentation
from score.models import Score 
from score.serializers import ScoreSerializer 

from common.is_authenticated import authenticated_required
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

# ---------------------------------
# GET View: Retrieve a list of scores
# ---------------------------------
@swagger_auto_schema(
        method="get",
        operation_description="Returns a paginated list of student scores. Admins see all scores, while non-admin users see only their own. Supports filtering by lesson and score value.",
        operation_summary="Get Scores value",
        manual_parameters=[
            openapi.Parameter(
                "lesson",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Enter a lesson id"
            ),
            openapi.Parameter(
                "score_value",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Enter a score value"
            )
        ]
)
@api_view(["GET"])
@authenticated_required
def scoreGetView(request, *args, **kwargs):
    """
    Retrieves a list of scores:
    - Admin users can see all scores.
    - Non-admin users can only see their own scores.
    - Supports filtering by lesson and score value.
    """
    user = request.user 
    # Determine the queryset based on user type
    queryset = Score.objects.filter(students=user) if (not user.is_staff) or (user.user_type != "admin") else Score.objects.all()

    # Apply filters based on query parameters
    filters = {
        "lesson": request.query_params.get("lesson"),
        "score_value": request.query_params.get("score_value")
    }
    filters = {k: v for k, v in filters.items() if v}  # Remove empty filters
    queryset = queryset.filter(**filters)

    # Paginate the results for better performance and usability
    paginator = PageNumberPagination()
    paginator.page_size = 10 
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = ScoreSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)

# ---------------------------------
# POST View: Create a new score
# ---------------------------------
@swagger_auto_schema(
    method="post",
    request_body=ScoreSerializer,
    operation_description="Allows teachers or admin users to create a new score entry. Validates input data and returns the created score upon success. Access is restricted to authenticated users with teacher or admin roles.",
    operation_summary="Post Scores",
    responses = {
        201: ScoreSerializer,
        400: "Invalid data",
        401: "Authenticated required"
    }
)
@api_view(["POST"])
@authenticated_required
def scorePostView(request):
    """
    Allows teachers or admin users to create a new score:
    - Validates the input data using the ScoreSerializer.
    - Returns the created score on success.
    - Restricted to authenticated users with teacher or admin roles.
    """
    user = request.user 

    # Check if the user has the required permissions
    if not user.is_staff:
        if (user.user_type != "teacher"):
            return Response(
                {"detail":"You are not allowed to create score"},
                status=status.HTTP_403_FORBIDDEN
            )
        
    # Validate and save the score data
    serializer = ScoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Score created successfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        # Return validation errors if the data is invalid
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# ---------------------------------
# PUT View: Update an existing score
# ---------------------------------
@swagger_auto_schema(
    method="put",
    operation_description="Allows authenticated teachers or admins to update an existing score using its ID. Returns updated data on success or appropriate error messages.",
    operation_summary="Updated Scores",
    request_body=ScoreSerializer,
    responses={
        200: ScoreSerializer,
        400: "Invalid data",
        401: "Authenticated required",
        403: "Forbidden",
        404: "Not found"
    }
)
@api_view(["PUT"])
@authenticated_required
def scorePutView(request, *args, **kwargs):
    """
    Updates an existing score:
    - Restricted to authenticated teachers or admin users.
    - Validates the input data and updates the score.
    - Returns the updated score on success or appropriate error messages.
    """
    user = request.user 
    # Check if the user has the required permissions
    if not user.is_staff:
        if (user.user_type != "teacher"):
            return Response(
                {"detail":"You are not allowed to updated score"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    # Retrieve the score by ID
    score_id = kwargs.get("score_value_id")
    try:
        score = Score.objects.get(id=score_id)
    except Score.DoesNotExist:
        # Return a 404 error if the score does not exist
        return Response(
            {"detail":"Score not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Validate and update the score data
    serializer = ScoreSerializer(score, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Score updated successfully!", "data":serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        # Return validation errors if the data is invalid
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# ---------------------------------
# DELETE View: Delete a score
# ---------------------------------
@swagger_auto_schema(
    method="delete",
    operation_description="Allows authenticated teachers or admins to delete a score using its ID. Returns a success message on deletion or appropriate error responses.",
    operation_summary="Deleted Scores",
    responses={
        204: "Deleted successfully",
        401: "Authenticated required",
        403: "Forbidden",
        404: "Not found"
    }
)
@api_view(["DELETE"])
@authenticated_required
def scoreDeleteView(request, *args, **kwargs):
    """
    Deletes a score:
    - Restricted to authenticated teachers or admin users.
    - Deletes the score by its ID.
    - Returns a success message or appropriate error responses.
    """
    user = request.user 
    # Check if the user has the required permissions
    if not user.is_staff:
        if user.user_type != "teacher":
            return Response(
                {"detail":"You are not allowed to deleted score"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    # Retrieve the score by ID
    score_id = kwargs.get("score_value_id")
    try:
        score = Score.objects.get(id=score_id)
    except Score.DoesNotExist:
        # Return a 404 error if the score does not exist
        return Response(
            {"detail":"Score not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Delete the score and return a success response
    score.delete()
    return Response(
        {"detail":"Score deleted successfully!"},
        status=status.HTTP_204_NO_CONTENT
    )