from django.urls import path 
from present_absent.views import getAttendingView, postAttendingView, putAttendingView

urlpatterns = [
    path("attending/", getAttendingView),
    path("attending/create/", postAttendingView),
    path("attending/<int:attending_id>/update/", putAttendingView),
]
