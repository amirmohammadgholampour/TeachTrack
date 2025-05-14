"""
Present/Absent Permissions
===========================
This module provides custom permission decorators for validating and managing attendance-related operations.
The following decorators are included:

1. `attending_validations`:
   - Validates the data provided for creating or updating attendance records.
   - Ensures that only authorized users (teachers or administrators) can register attendance.
   - Verifies that the user being marked for attendance is a student and is active.
   - Checks for mismatches between the selected classroom and the user.
   - Prevents duplicate attendance records for the same user and date.
   - Disallows recording attendance for future dates.

2. `check_attending_exist`:
   - Ensures that the attendance record exists before performing operations like update or delete.
   - Retrieves the attendance record and passes it to the view function.

Key Features:
- Provides robust validation for attendance operations.
- Ensures data integrity and prevents unauthorized access.
"""

from functools import wraps 
from rest_framework.response import Response 
from rest_framework import status 
from user.models import User
from classroom.models import ClassRoom
from datetime import datetime
from present_absent.models import PresentAbsent 

# Decorator to validate attendance data
def attending_validations(view_func):
    """
    Validates the data for creating or updating attendance records.
    - Ensures only teachers or administrators can register attendance.
    - Verifies that the user being marked is a student and is active.
    - Checks for mismatches between the classroom and the user.
    - Prevents duplicate attendance records for the same user and date.
    - Disallows attendance for future dates.
    """
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        classroom_id = request.data.get("classroom")
        user_id = request.data.get("user")
        user = request.user
        
        # Check if the user is authorized to register attendance
        if (not user.user_type in ["admin"]) and (user.is_staff != True):
            return Response(
                {"detail":"Only administrators have the right to register student attendance."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if the user being marked is a student
        user = User.objects.filter(id=user_id).first()
        if not user or user.user_type != "student":
            return Response(
                {"detail": "Only students can take attendance."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the student is active
        if user.is_active == False:
            return Response(
                {"detail":"This student is inactive."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for mismatches between the classroom and the user
        if not ClassRoom.objects.filter(id=classroom_id, students__id=user_id).exists():
            return Response(
                {"detail": "Mismatch between selected classroom and user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for duplicate attendance records for the same user and date
        req_date = datetime.strptime(request.data.get("date"), "%Y-%m-%d")
        main_date = PresentAbsent.objects.filter(user=user_id, date=req_date)
        if main_date.exists():
            return Response(
                {"detail":"This user with this date is already exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Disallow attendance for future dates
        present_date = datetime.today()
        if req_date > present_date:
            return Response(
                {"detail":"You cannot record attendance for a future date."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return view_func(request, *args, **kwargs)
    return _wrap_view

# Decorator to check if an attendance record exists
def check_attending_exist(view_func):
    """
    Ensures that the attendance record exists before performing operations.
    - Retrieves the attendance record by ID.
    - Passes the attendance record to the view function.
    """
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        attending_id = kwargs.get("attending_id")
        try:
            # Retrieve the attendance record
            attending = PresentAbsent.objects.get(id=attending_id)
        except PresentAbsent.DoesNotExist:
            return Response(
                {"detail":"Attending not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Pass the attendance record to the view function
        kwargs["attending"] = attending
        return view_func(request, *args, **kwargs)
    return _wrap_view