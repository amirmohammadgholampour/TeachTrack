from django.urls import path 
from event.views import eventGetView, eventPostView, eventPutView, eventDeleteView
from event.registration_views import registerGetView, registerPostView, registerPutView, registerDeleteView

urlpatterns = [
    path("event/", eventGetView, name="Get Events"),
    path("event/create/", eventPostView, name="Post Event"),
    path("event/<int:event_id>/update/", eventPutView, name="Put Event"),
    path("event/<int:event_id>/delete/", eventDeleteView, name="Delete Event"),

    path("event/register/", registerGetView, name="Get Registration"),
    path("event/register/create/", registerPostView, name="Post Registration"),
    path("event/register/<int:registration_id>/update/", registerPutView, name="Put Registration"),
    path("event/register/<int:registration_id>/delete/", registerDeleteView, name="Delete Registration")
]
