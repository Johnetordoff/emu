from django.contrib import admin
from canary.views import (
    ReportSpamView
)

from django.urls import path



urlpatterns = [
    path("report/", ReportSpamView.as_view(), name="report_spam"),
]
