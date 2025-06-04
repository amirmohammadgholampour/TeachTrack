from django.urls import path 
from classroom.views import classroomGetView, classroomPostView, classroomPutView, classroomDeleteView

urlpatterns = [
    path('classroom/', classroomGetView, name="Get classroom view"),
    path('classroom/create/', classroomPostView, name="Post classroom view"),
    path('classroom/<int:classroom_id>/update/', classroomPutView, name="Put classroom view"),
    path('classroom/<int:classroom_id>/delete/', classroomDeleteView, name="Delete classroom view"),
]
