from present_absent.models import PresentAbsent 
from classroom.models import ClassRoom
from present_absent.serializers import PresentAbsentSerializer
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status 
from datetime import datetime 

@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "user",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            "status",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            "classroom",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            "date",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            "search",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(["GET"])
@authenticated_required
def getAttendingView(request, *args, **kwargs):
    req_user = request.user 
    queryset = PresentAbsent.objects.filter(user=req_user) if req_user.user_type != "admin" else PresentAbsent.objects.all() 
    filters = {
        "user__username": request.query_params.get("user"),
        "status": request.query_params.get("status"),
        "classroom__name": request.query_params.get("classroom"),
        "date": request.query_params.get("date")
    }
    filters = {k:v for k,v in filters.items() if v}
    queryset = queryset.filter(**filters)

    search_query = request.query_params.get("search")
    if search_query:
        queryset = queryset.filter(user__username=search_query)

    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = PresentAbsentSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)
