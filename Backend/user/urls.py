from django.urls import path 
from user.views import userGetView, userCreateView, userUpdateView, userDeleteView

urlpatterns = [
    path("users/", userGetView, name="user-get"),
    path("users/create/", userCreateView, name="user-create"),
    path("users/<int:user_id>/update/", userUpdateView, name="user-update"),
    path("users/<int:user_id>/delete/", userDeleteView, name="user-delete"),

]
