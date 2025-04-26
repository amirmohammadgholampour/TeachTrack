from reportcard.models import ReportCard 
from reportcard.serializers import ReportCardSerializer
from common.is_authenticated import authenticated_required
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
            "discplinary_status",
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
        "class-room": request.query_params.get("class_room"),
        "disciplinary-status": request.query_params.get("discplinary_status")
    }
    filters = {k:v for k,v in filters.items() if v}
    queryset = queryset.filter(**filters)

    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = ReportCardSerializer(paginated_queryset, many=True)
    return paginated.get_paginated_response(serializer.data)