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
from datetime import datetime
from django.db.models import Q 

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
def postAttendanceApprovalView(request, *args, **kwargs):
    req_user = request.user 
    if (not req_user.user_type in ["admin", "teacher"]) and (req_user.is_staff != True):
        return Response(
            {"detail":"Only teachers and administrators have the right to register student attendance."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student_id = request.data.get("student")
    user = User.objects.filter(id=student_id).first()
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
    
    classroom_id = request.data.get("classroom")
    if not ClassRoom.objects.filter(id=classroom_id, students__id=student_id).exists():
        return Response(
            {"detail": "Mismatch between selected classroom and user."},
            status=status.HTTP_400_BAD_REQUEST
        )

    req_date = datetime.strptime(request.data.get("date"), "%Y-%m-%d")
    main_date = AttendanceApproval.objects.filter(student=student_id, date=req_date)
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