from django.urls import path 
from present_absent.views import getAttendingView, postAttendingView

urlpatterns = [
    path("attending/", getAttendingView),
    path("attending/create/", postAttendingView),
]
