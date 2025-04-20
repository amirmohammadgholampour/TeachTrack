"""
User API
========
This module provides CRUD (Create, Read, Update, Delete) operations for managing users in the system.
The API includes the following endpoints:
1. GET `/users/` - Retrieve a list of users with optional filters.
2. POST `/users/create/` - Create a new user with validation and password hashing.
3. PUT `/users/<user_id>/update/` - Update an existing user's information.
4. DELETE `/users/<user_id>/delete/` - Delete a user account.

Key Features:
- Staff users have elevated permissions to manage all users.
- Non-staff users can only view, update, or delete their own accounts.
- Validation for phone numbers and national codes.
- Secure password handling with hashing.
- Swagger documentation for API endpoints.
"""

from user.models import User
from user.serializers import UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from django.conf import settings

# Helper function to validate user input fields
# This function checks if required fields are present, numeric, and of the correct length.
def validate_user_input(data, required_fields):
    """
    Validates user input for required fields.
    Args:
        data (dict): The input data to validate.
        required_fields (dict): A dictionary where keys are field names and values are required lengths.
    Returns:
        str: An error message if validation fails, or None if validation passes.
    """
    for field, length in required_fields.items():
        value = data.get(field)
        if not value:
            return f"{field.replace('_', ' ').capitalize()} is required."
        if not value.isdigit():
            return f"{field.replace('_', ' ').capitalize()} must be digits."
        if len(value) != length:
            return f"{field.replace('_', ' ').capitalize()} must be {length} digits."
    return None

# API endpoint to retrieve a list of users
@swagger_auto_schema(
    method='get',
    operation_summary="Get user list",
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_QUERY, description="Filter by username", type=openapi.TYPE_STRING),
        openapi.Parameter('phone_number', openapi.IN_QUERY, description="Filter by phone number", type=openapi.TYPE_STRING),
        openapi.Parameter('national_code', openapi.IN_QUERY, description="Filter by national code", type=openapi.TYPE_STRING),
    ]
)
@api_view(["GET"])
def userGetView(request, *args, **kwargs):
    """
    Retrieves a list of users based on filters.
    - Staff users can view all users.
    - Non-staff users can only view their own data.
    """
    user = request.user
    if not user.is_authenticated:
        return Response(
            {"detail": "Please sign-in."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Staff users can view all users; others can only view their own data.
    queryset = User.objects.filter(id=user.id) if not user.is_staff else User.objects.all()

    # Apply filters based on query parameters
    filters = {
        "username__icontains": request.query_params.get("username"),
        "phone_number__icontains": request.query_params.get("phone_number"),
        "national_code__icontains": request.query_params.get("national_code"),
    }
    filters = {k: v for k, v in filters.items() if v}  # Remove empty filters
    queryset = queryset.filter(**filters)

    # Paginate the results for better performance
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = UserSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)

# API endpoint to create a new user
@swagger_auto_schema(
    method='post',
    operation_summary="Create a new user",
    request_body=UserSerializer,
    responses={201: UserSerializer(), 400: "Bad Request", 403: "Forbidden"}
)
@api_view(["POST"])
def userCreateView(request, *args, **kwargs):
    """
    Creates a new user.
    - cheack user authenticated.
    - Validates phone number and national code.
    - Checks for admin and teacher passwords if applicable.
    - Hashes the password before saving.
    """
    user = request.user 
    # Users just can authenticated for one account
    if user.is_authenticated:
        return Response(
            {"detail":"You already have an account."},
            status=status.HTTP_403_FORBIDDEN 
        )
    
    data = request.data.copy()
    # Validate phone number and national code
    validation_error = validate_user_input(data, {"phone_number": 11, "national_code": 10})
    if validation_error:
        return Response(
            {"detail": validation_error}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check for admin and teacher passwords
    if data.get("user_type") == "admin" and data.get("password") != settings.ADMIN_PASSWORD:
        return Response(
            {"detail": "The password of admin is incorrect."}, 
            status=status.HTTP_403_FORBIDDEN
        )

    if data.get("user_type") == "teacher" and data.get("password") != settings.TEACHER_PASSWORD:
        return Response(
            {"detail": "The password of teacher is incorrect."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Hash the password before saving
    if "password" in data:
        data["password"] = make_password(data["password"])

    # Serialize and save the user data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "User created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail": "Invalid data", "errors": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to update an existing user
@swagger_auto_schema(
    method="put",
    operation_summary="Update a user",
    request_body=UserSerializer,
    responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
)
@api_view(["PUT"])
def userUpdateView(request, *args, **kwargs):
    """
    Updates an existing user.
    - Only staff users or the user themselves can update the data.
    - Validates phone number and national code.
    - Hashes the password if it is being updated.
    """
    user = request.user
    if not user.is_authenticated:
        return Response(
            {"detail": "Please sign-in."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Retrieve user_id from URL parameters
    user_id = kwargs.get("user_id")
    if not user_id:
        return Response(
            {"detail": "A valid User ID is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the target user exists
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"detail": "User not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Ensure only staff or the user themselves can update the data
    if not user.is_staff and target_user.id != user.id:
        return Response(
            {"detail": "You are not allowed to update this user."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Validate phone number and national code
    data = request.data.copy()
    validation_error = validate_user_input(data, {"phone_number": 11, "national_code": 10})
    if validation_error:
        return Response(
            {"detail": validation_error}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check for admin and teacher passwords
    if data.get("user_type") == "admin" and data.get("password") != settings.ADMIN_PASSWORD:
        return Response(
            {"detail": "The password of admin is incorrect."},
            status=status.HTTP_403_FORBIDDEN
        )

    if data.get("user_type") == "teacher" and data.get("password") != settings.TEACHER_PASSWORD:
        return Response(
            {"detail": "The password of teacher is incorrect."}, 
            status=status.HTTP_403_FORBIDDEN
        )

    # Hash the password if it is being updated
    if "password" in data:
        data["password"] = make_password(data["password"])

    # Serialize and save the updated data
    serializer = UserSerializer(target_user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "User updated successfully", "data": serializer.data}, 
            status=status.HTTP_200_OK
            )
    else:
        return Response(
            {"detail": "Invalid data", "errors": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )

# API endpoint to delete a user
@swagger_auto_schema(
    method="delete",
    operation_summary="Delete a user",
    responses={204: "No Content", 403: "Forbidden", 404: "Not Found"}
)
@api_view(["DELETE"])
def userDeleteView(request, *args, **kwargs):
    """
    Deletes a user.
    - Only staff users or the user themselves can delete the account.
    """
    user = request.user
    if not user.is_authenticated:
        return Response(
            {"detail": "Please sign-in."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Retrieve user_id from URL parameters
    user_id = kwargs.get("user_id")
    if not user_id:
        return Response(
            {"detail": "A valid User ID is required."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the target user exists
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"detail": "User not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # Ensure only staff or the user themselves can delete the account
    if not user.is_staff and target_user.id != user.id:
        return Response(
            {"detail": "You are not allowed to delete this user."}, 
            status=status.HTTP_403_FORBIDDEN
        )

    # Delete the target user
    target_user.delete()
    return Response(
        {"detail": "User deleted successfully!"}, 
        status=status.HTTP_204_NO_CONTENT
    )