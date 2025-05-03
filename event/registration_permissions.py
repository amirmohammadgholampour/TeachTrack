from functools import wraps 
from rest_framework.response import Response 
from rest_framework import status 
from event.models import Registration

def validations_registeration(view_func):
    @wraps(view_func) 
    def _wrap_view(request, *args, **kwargs):
        event_capacity = request.data.get("event__capacity")
        if event_capacity == "completed":
            return Response(
                {"detail":"Compacity for this event is full"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        event_status = request.data.get("event__status")
        if event_status in ["held", "in_progress"]:
            return Response(
                {"detail":"This event is not open for registrations"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        req_user=request.user
        if Registration.objects.filter(user=req_user).count() >= 3:
            return Response(
                {"detail":"You are not allowed to registration"},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)
    return _wrap_view

def check_registration_exist(view_func):
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        register_id = kwargs.get("registration_id")
        try:
            registration = Registration.objects.get(id=register_id)
        except Registration.DoesNotExist:
            return Response(
                {"detail":"Registration not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        kwargs["registration"] = registration
        return view_func(request, *args, **kwargs)
    return _wrap_view