from django.urls import path 
from present_absent.views import (
    getAttendingView,
    postAttendingView,
    putAttendingView,
    deleteAttendingView
)
from present_absent.attendance_approvald_views import (
    getAttendanceApprovalView,
    postAttendanceApprovalView,
    putAttendanceApprovaldView,
    deleteAttendanceApprovalView
)
from present_absent.attendance_review_views import (
    getAttendanceReview
)

urlpatterns = [
    path("attending/", getAttendingView),
    path("attending/create/", postAttendingView),
    path("attending/<int:attending_id>/update/", putAttendingView),
    path("attending/<int:attending_id>/delete/", deleteAttendingView),

    path("attending/approval/", getAttendanceApprovalView),
    path("attending/approval/create/", postAttendanceApprovalView),
    path("attending/approval/<int:attendance_id>/update/", putAttendanceApprovaldView),
    path("attending/approval/<int:attendance_id>/delete/", deleteAttendanceApprovalView),

    path("attending/review/", getAttendanceReview),
]
