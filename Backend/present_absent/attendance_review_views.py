from present_absent.models import AttendanceReview, AttendanceApproval
from present_absent.serializers import AttendanceReviewSerializer 
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status 
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi 
from rest_framework.pagination import PageNumberPagination 
from django.db.models import Q 
from django.core.exceptions import FieldError

@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("review-status", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("reviewed-by", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("reviewed-at", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("attending-approval-date", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("order_by", openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ]
)
@api_view(["GET"])
@authenticated_required
# @admin_required
def getAttendanceReview(request, *args, **kwargs):
    req_user = request.user 
    if not req_user.user_type in ["teacher", "admin"]:
        return Response(
            {"detail":"You are not alllowed to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )

    if req_user.user_type != "admin":
        queryset = AttendanceReview.objects.filter(attending_approval__teacher = req_user.id)
    else:
        queryset = AttendanceReview.objects.all()

    filters = {
        "review_status": request.query_params.get("review-status"),
        "reviewed_by": request.query_params.get("reviewed-by"),
        "reviewed_at__date": request.query_params.get("reviewed-at"),
        "attending_approval__date": request.query_params.get("attending-approval-date"),
    }
    filters = {k:v for k,v in filters.items() if v}
    queryset = queryset.filter(**filters)

    search_query = request.query_params.get("search")
    if search_query:
        queryset = queryset.filter(
            Q(attending_approval__student__username__icontains=search_query) |
            Q(attending_approval__teacher__username__icontains=search_query) |
            Q(attending_approval__classroom__name__icontains=search_query) |
            Q(reviewed_by__username__icontains=search_query)
        )

    try:
        order_by = request.query_params.get("order_by")
        if order_by:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by("-reviewed_at")
    except FieldError as e:
        return Response(
            {"detail":f"Invalid order field: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request) 
    serializer = AttendanceReviewSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)

@swagger_auto_schema(
    method="post",
    request_body=AttendanceReviewSerializer
)
@api_view(["POST"])
@authenticated_required
@admin_required 
def postAttendanceReview(request, *args, **kwargs):
    attendance_approval_id = request.data.get("attending_approval")
    attendance_approval = AttendanceApproval.objects.filter(id=attendance_approval_id)
    if not attendance_approval.exists():
        return Response(
            {"detail":"AttendanceApproval not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AttendanceReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Attendance Review created successfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail":"Invalid data.", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )