from present_absent.models import PresentAbsent 
from present_absent.serializers import PresentAbsentSerializer
from common.is_authenticated import authenticated_required
from common.is_admin import admin_required
from rest_framework.decorators import api_view
from present_absent.permissions import attending_validations, check_attending_exist
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status 

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
@attending_validations
def postAttendingView(request):
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
    
@swagger_auto_schema(
    method="put",
    request_body=PresentAbsentSerializer
)
@api_view(["PUT"])
@authenticated_required
@check_attending_exist
@attending_validations
def putAttendingView(request, *args, **kwargs):
    attending = kwargs.get("attending")
    serializer = PresentAbsentSerializer(attending, data=request.data, partial=True)
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

@swagger_auto_schema(
    method="delete"
)
@api_view(["DELETE"])
@authenticated_required
@check_attending_exist
@admin_required
def deleteAttendingView(request, *args, **kwargs):
    attending = kwargs.get("attending")
    attending.delete()
    return Response(
        {"detail":"Attending deleted successfully!"},
        status=status.HTTP_204_NO_CONTENT
    )