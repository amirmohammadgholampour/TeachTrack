from present_absent.models import PresentAbsent 
from classroom.models import ClassRoom
from user.models import User
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

@swagger_auto_schema(
    method="post",
    request_body=PresentAbsentSerializer
)
@api_view(["POST"])
@authenticated_required
def postAttendingView(request):
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
    
    serializer = PresentAbsentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Attending created succussfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(["PUT"])
@authenticated_required
def putAttendingView(request, *args, **kwargs):

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

    attending_id = kwargs.get("attending_id")
    try:
        PresentAbsent.objects.get(id=attending_id)
    except PresentAbsent.DoesNotExist:
        return Response(
            {"detail":"Attending not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PresentAbsentSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Attending updated successfully!", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(["DELETE"])
@authenticated_required
def deleteAttendingView(request, *args, **kwargs):
    pass 