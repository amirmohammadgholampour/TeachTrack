from present_absent.models import AttendanceApproval, PresentAbsent 
from present_absent.serializers import AttendanceApprovalSerializer
from user.models import User 
from classroom.models import ClassRoom
from rest_framework.decorators import api_view 
from rest_framework import status 
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from common.is_authenticated import authenticated_required
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi 
from django.db.models import Q 
from present_absent.permissions import attending_validations, check_attending_exist

@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("status", openapi.IN_QUERY, type=openapi.TYPE_STRING),
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
            Q(teacher__username=search_query) |
            Q(student__username=search_query) |
            Q(classroom__name=search_query)
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

@swagger_auto_schema(
    method="post",
    request_body=AttendanceApprovalSerializer,
)
@api_view(["POST"])
@authenticated_required
@attending_validations
def postAttendanceApprovalView(request, *args, **kwargs):
    serializer = AttendanceApprovalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Attendance created successfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail":"Invalid data.", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        ) 
    
@swagger_auto_schema(
    method="put",
    request_body=AttendanceApprovalSerializer
)
@api_view(["PUT"])
@authenticated_required 
@check_attending_exist
@attending_validations
def putAttendanceApprovaldView(request, *args, **kwargs):
    attendance = kwargs.get("attendance")
    serializer = AttendanceApprovalSerializer(attendance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"AttendanceApproval updated successfully!","data":serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail":"Invalid data.", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )