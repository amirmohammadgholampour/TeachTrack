from django.urls import path
from gamification.views import (
    StudentProfileView,
    
)
urlpatterns = [
    path('gamification/student-profile/', StudentProfileView.as_view(), name='student_profile'),
]
