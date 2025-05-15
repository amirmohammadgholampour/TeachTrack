from present_absent.models import AttendanceApproval
from present_absent.serializers import AttendanceApprovalSerializer
from rest_framework.decorators import api_view 
from rest_framework import status 
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from common.is_authenticated import authenticated_required
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi 

@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("status_requested", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("date", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("order_by", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ]
)
@api_view(["GET"])
@authenticated_required
def getAttendanceApprovalView(request, *args, **kwargs):
    req_user = request.user
    if (not req_user.user_type in ["admin", "teacher"]) and (req_user.is_staff != True):
        return Response(
            {"detail":"You are not allowed to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    queryset = AttendanceApproval.objects.all()

    filters = {
        "status_requested": request.query_params.get("status"),
        "date": request.query_params.get("date"),
    }
    filters = {k:v for k,v in filters.items() if v}
    queryset = queryset.filter(**filters) 

    search_query = request.query_params.get("search")
    if search_query:
        queryset = queryset.filter(
            teacher__username=search_query,
            student__username=search_query,
            classroom__name=search_query
        )
    
    order_by = request.query_params.get("order_by")
    if order_by:
        queryset = queryset.order_by(order_by)
    else:
        queryset = queryset.order_by("-date")

    paginated = PageNumberPagination()
    paginated.page_size = 10 
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = AttendanceApprovalSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)