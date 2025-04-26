from django.urls import path 
from reportcard.views import reportcardGetView 

urlpatterns = [
    path("reportcard/", reportcardGetView, name="Get ReportCards")
]
