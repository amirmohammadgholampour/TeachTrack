from event.models import Registration 
from event.serializers import RegistrationSerializer
from rest_framework.decorators import api_view
from common.is_authenticated import authenticated_required
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 
from django.db.models import Q 
from datetime import datetime, date


@api_view(["GET"])
@authenticated_required
def registerGetView(request, *args, **kwargs):
    user = request.user 
    queryset = Registration.objects.filter(id=user.id) if user.user_type != "admin" else Registration.objects.all()

    search = request.query_params.get("search")
    if search:
        queryset = queryset.filter(
            Q(user__username__icontains=search) |
            Q(event__name__icontains=search)
        )

    filters = {
        "event": request.query_params.get("event"),
        "user": request.query_params.get("user"),
        "event__status": request.query_params.get("status")
    }
    filters = {k: v for k,v in filters.items() if v}
    queryset = queryset.filter(**filters)

    future_event = request.query_params.get("future")
    if future_event and future_event.lower() == "true":
        user_date = date.today()
        queryset = queryset.filter(event__date__gte=user_date)

    past_event = request.query_params.get("past")
    if past_event and past_event.lower() == "true":
        user_date = date.today()
        queryset = queryset.filter(event__date__lte=user_date)

    today_register = request.query_params.get("today_register")
    if today_register and today_register.lower() == "true":
        user_date = date.today()
        queryset = queryset.filter(register_at=user_date)

    ordering = request.query_params.get("ordering")
    allowed_fields = ["register_at", "-register_at"]
    if ordering in allowed_fields:
        queryset = queryset.order_by(ordering)

    paginated = PageNumberPagination()
    paginated.page_size = 10
    paginated_queryset = paginated.paginate_queryset(queryset, request)
    serializer = RegistrationSerializer(paginated_queryset, many=True) 
    return paginated.get_paginated_response(serializer.data)

# @swagger_auto_schema(
#     method="post",
#     request_body=RegistrationSerializer
# )
# @api_view(["POST"])
# @authenticated_required
# def registerPostView(request):
#     serializer = RegistrationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             {"detail":"Registered successfully!", "data":serializer.data},
#             status=status.HTTP_201_CREATED
#         )
#     else:
#         return Response(
#             {"detail":"Invalid data", "errors":serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )