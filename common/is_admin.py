from functools import wraps 
from rest_framework.response import Response 
from rest_framework import status 

def admin_required(view_func):
    @wraps(view_func)
    def _wraps_view(request, *args, **kwargs):
        user = request.user 
        if (not user.is_authenticated) or (user.user_type != "admin"):
            return Response(
                {"detail":"You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)
    return _wraps_view