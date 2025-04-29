from score.models import Score
from reportcard.models import ReportCard 
from reportcard.serializers import ReportCardSerializer
from reportcard.serializers import ReportCardSerializer
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    user_id = request.data.get("user")
    score_ids = request.data.get("scores")

    if not user_id or not score_ids:
        return Response(
            {"detail": "User ID and Scores are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    students_ids = Score.objects.filter(id__in=score_ids).values_list("students", flat=True).distinct()

    if students_ids.count() != 1 or students_ids.first() != user_id:
        return Response(
            {"detail": "Mismatch between selected scores and user."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ReportCardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"Report Card created successfully!", "data":serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@swagger_auto_schema(
    method="put",
    request_body=ReportCardSerializer
)
@api_view(["PUT"])
@authenticated_required
@admin_required
def reportcardPutView(request, *args, **kwargs):
    user_id = request.data.get("user")
    score_ids = request.data.get("scores")

    if not user_id or not score_ids:
        return Response(
            {"detail": "User ID and Scores are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    students_ids = Score.objects.filter(id__in=score_ids).values_list("students", flat=True).distinct()

    if students_ids.count() != 1 or students_ids.first() != user_id:
        return Response(
            {"detail": "Mismatch between selected scores and user."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    reportcard_id = kwargs.get("reportcard_id")
    try:
        reportcard = ReportCard.objects.get(id=reportcard_id)
    except ReportCard.DoesNotExist:
        return Response(
            {"detail":"ReportCard not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ReportCardSerializer(reportcard, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail":"ReportCard updated successfully!", "data":serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail":"Invalid data", "errors":serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )