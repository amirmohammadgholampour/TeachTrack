"""
Report Card Permissions
=======================
This module provides custom permission decorators for validating user input and ensuring the existence of report cards.

Functions:
1. validate_user_and_scores: Validates that the provided user ID and scores are correct and consistent.
2. check_reportcard_exists: Ensures that the specified report card exists before proceeding with the view.

Key Features:
- Ensures data integrity by validating relationships between users and scores.
- Prevents operations on non-existent report cards.
- Returns appropriate error responses for invalid or missing data.
"""

from rest_framework.response import Response 
from rest_framework import status 
from functools import wraps
from reportcard.models import ReportCard 
from user.models import User 
from score.models import Score 

# Decorator to validate user ID and associated scores
def validate_user_and_scores(view_func):
    """
    Validates that the provided user ID and scores are correct and consistent.
    - Checks if the user ID and scores are provided in the request data.
    - Ensures the user exists in the database.
    - Verifies that all selected scores belong to the specified user.

    Args:
        view_func (function): The view function to wrap.

    Returns:
        Response: An error response if validation fails, or proceeds to the view if validation passes.
    """
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        user_id = request.data.get("user")
        score_ids = request.data.get("scores")

        # Check if user ID and scores are provided
        if not user_id or not score_ids:
            return Response({"detail": "User ID and Scores are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists
        if not User.objects.filter(id=user_id).exists():
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate that all scores belong to the specified user
        students_ids = Score.objects.filter(id__in=score_ids).values_list("students", flat=True).distinct()
        if students_ids.count() != 1 or students_ids.first() != user_id:
            return Response({"detail": "Mismatch between selected scores and user."}, status=status.HTTP_400_BAD_REQUEST)

        return view_func(request, *args, **kwargs)
    return _wrap_view

# Decorator to check if a report card exists
def check_reportcard_exists(view_func):
    """
    Ensures that the specified report card exists before proceeding with the view.
    - Retrieves the report card by its ID from the URL parameters.
    - If the report card does not exist, returns a 404 error response.

    Args:
        view_func (function): The view function to wrap.

    Returns:
        Response: An error response if the report card does not exist, or proceeds to the view if it does.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        reportcard_id = kwargs.get("reportcard_id")
        try:
            # Attempt to retrieve the report card
            reportcard = ReportCard.objects.get(id=reportcard_id)
        except ReportCard.DoesNotExist:
            return Response(
                {"detail": "ReportCard not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        # Add the report card to the kwargs for use in the view
        kwargs["reportcard"] = reportcard
        return view_func(request, *args, **kwargs)
    return _wrapped_view