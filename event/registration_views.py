from event.models import Registration 
from event.serializers import RegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 

@api_view(["GET"])
def registerGetView(request, *args, **kwargs):
    pass 