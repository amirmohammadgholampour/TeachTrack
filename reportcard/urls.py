from django.urls import path 
from reportcard.views import reportcardGetView , reportcardPostView, reportcardPutView

urlpatterns = [
    path("reportcard/", reportcardGetView, name="Get ReportCards"),
    path("reportcard/create/", reportcardPostView, name="Post ReportCards"),
    path("reportcard/<int:reportcard_id>/update", reportcardPutView, name="Put ReportCards"),
]
