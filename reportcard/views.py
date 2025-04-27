from score.models import Score
from reportcard.models import ReportCard 
from reportcard.serializers import ReportCardSerializer
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def calculate_average(user):
    scores = Score.objects.filter(students=user)
    total_score = sum(score.score_value for score in scores)
    lesson_count = scores.values("lesson").distinct().count()

    if lesson_count == 0:
        return 0

    average = total_score / lesson_count
    return round(average, 2)


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "class_room",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Enter classroom of student"
        ),
        openapi.Parameter(
            "disciplinary_status",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Enter a discplinary status of student(very good, good, normal, bad, very bad)"
        )
    ]
)
@api_view(["GET"])
@authenticated_required
def reportcardGetView(request, *args, **kwargs):
    user = request.user 
    if (not user.is_staff) or (user.user_type != "admin"):
        queryset = ReportCard.objects.filter(user=user)
    else:
        queryset = ReportCard.objects.all()
    
    filters = {
        "class_room_id": request.query_params.get("class_room"),
        "disciplinary_status__icontains": request.query_params.get("disciplinary_status")
    }
    filters = {k: v for k, v in filters.items() if v} 
    queryset = queryset.filter(**filters)

    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = ReportCardSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)

@swagger_auto_schema(
    method="post",
    request_body=ReportCardSerializer,
    responses={
        201: ReportCardSerializer,
        401: "Authenticated required",
        400: "Invalid data",
        403: "Forbidden",
    }
)
@api_view(["POST"])
@authenticated_required
@admin_required
def reportcardPostView(request):
    user = request.user 
    average = calculate_average(user)
    serializer = ReportCardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(grade=average)
        return Response(
            {"detail":"Report Card created successfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )