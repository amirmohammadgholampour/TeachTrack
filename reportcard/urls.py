from django.urls import path 
from reportcard.views import reportcardGetView , reportcardPostView

urlpatterns = [
    path("reportcard/", reportcardGetView, name="Get ReportCards"),
    path("reportcard/create/", reportcardPostView, name="Post ReportCards")
]
