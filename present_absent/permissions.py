from functools import wraps 
from rest_framework.response import Response 
from rest_framework import status 
from user.models import User
from classroom.models import ClassRoom
from datetime import datetime
from present_absent.models import PresentAbsent 

def attending_validations(view_func):
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        classroom_id = request.data.get("classroom")
        user_id = request.data.get("user")
        user = request.user
        
        if (not user.user_type in ["admin", "teacher"]) and (user.is_staff != True):
            return Response(
                {"detail":"Only teachers and administrators have the right to register student attendance."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = User.objects.filter(id=user_id).first()
        if not user or user.user_type != "student":
            return Response(
                {"detail": "Only students can take attendance."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user.is_active == False:
            return Response(
                {"detail":"This student is inactive."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not ClassRoom.objects.filter(id=classroom_id, students__id=user_id).exists():
            return Response(
                {"detail": "Mismatch between selected classroom and user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        req_date = datetime.strptime(request.data.get("date"), "%Y-%m-%d")
        main_date = PresentAbsent.objects.filter(user=user_id, date=req_date)
        if main_date.exists():
            return Response(
                {"detail":"This user with this date is already exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        present_date = datetime.today()
        if req_date > present_date:
            return Response(
                {"detail":"You cannot record attendance for a future date."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return view_func(request, *args, **kwargs)
    return _wrap_view

def check_attending_exist(view_func):
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        attending_id = kwargs.get("attending_id")
        try:
            attending = PresentAbsent.objects.get(id=attending_id)
        except PresentAbsent.DoesNotExist:
            return Response(
                {"detail":"Attending not found."},
            status=status.HTTP_404_NOT_FOUND
            )
        
        kwargs["attending"] = attending
        return view_func(request, *args, **kwargs)
    return _wrap_view