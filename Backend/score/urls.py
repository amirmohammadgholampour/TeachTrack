from django.urls import path 
from score.views import scoreGetView, scorePostView, scorePutView, scoreDeleteView

urlpatterns = [
    path("score/", scoreGetView, name="Get scores"),
    path("score/created/", scorePostView, name="Post scores"),
    path("score/<int:score_value_id>/update/", scorePutView, name="Put scores"),
    path("score/<int:score_value_id>/delete/", scoreDeleteView, name="Delete scores")
]
