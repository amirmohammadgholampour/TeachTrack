from rest_framework.views import APIView
from rest_framework.decorators import api_view
from common.is_authenticated import authenticated_required
from rest_framework.response import Response
from rest_framework import status
from gamification.models import StudentProfile, EventType, StudentEvent
from gamification.serializers import (
    StudentProfileSerializer,
    EventTypeSerializer, 
    StudentEventSerializer
)
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from common.is_admin import admin_required

class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "total_point",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Filter by total points"
            ),
            openapi.Parameter(
                "level",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Filter by level"
            ),
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Search by username or name"
            ),
            openapi.Parameter(
                "order_by",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Order by field"
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.user_type in ["admin", "student"]:
            return Response(
                {"detail":"Only students can view their profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if (user.user_type != "admin") and (user.is_staff != True):
            queryset = StudentProfile.objects.filter(students=user)
        else:
            queryset = StudentProfile.objects.all()

        filters = {
            "total_point": request.query_params.get("total_point"),
            "level": request.query_params.get("level")
        }
        filters = {k: v for k, v in filters.items() if v }
        queryset = queryset.filter(**filters)

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                students__username__icontains=search,
                student__first_name__icontains=search,
                student__last_name__icontains=search
            )
        
        order_by = request.query_params.get("order_by")
        if order_by:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by("-total_point")
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = StudentProfileSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(
        request_body=StudentProfileSerializer,
        responses={
            201: "created",
            400: "bad request",
            401: "Authenticated required",
            403: "Forbidden",
        }
    )
    @admin_required
    def post(self, request):
        serializer = StudentProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail":"StudentProfile created successfully!", "data":serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"detail":"Invalid data", "errors":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
@api_view(["GET"])
@authenticated_required
def getBestStudentInSchool(request, *args, **kwargs):
    queryset = StudentProfile.objects.order_by("-level", "-total_point")[:3]
    serializer = StudentProfileSerializer(queryset, many=True) 
    return Response(serializer.data)