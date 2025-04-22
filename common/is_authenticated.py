from functools import wraps 
from rest_framework.response import Response 
from rest_framework import status 

def authenticated_required(view_func):
    @wraps(view_func)
    def _wraps_view(request, *args, **kwargs):
        user = request.user 
        if not user.is_authenticated:
            return Response(
                {"detail":"Authenticated required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)
    return _wraps_view