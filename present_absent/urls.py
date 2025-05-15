from django.urls import path 
from present_absent.views import (
    getAttendingView,
    postAttendingView,
    putAttendingView,
    deleteAttendingView
)
from present_absent.attendance_approvald_views import (
    getAttendanceApprovalView
)

urlpatterns = [
    path("attending/", getAttendingView),
    path("attending/create/", postAttendingView),
    path("attending/<int:attending_id>/update/", putAttendingView),
    path("attending/<int:attending_id>/delete/", deleteAttendingView),

    path("attending/approval/", getAttendanceApprovalView),
]
