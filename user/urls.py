from django.urls import path 
from user.views import get_user_list

urlpatterns = [
    path("", get_user_list)
]
