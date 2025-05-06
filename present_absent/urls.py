from django.urls import path 
from present_absent.views import getAttendingView

urlpatterns = [
    path("attending/", getAttendingView),
]
