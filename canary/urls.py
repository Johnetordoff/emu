from django.contrib import admin
from canary.views import (
    ReportSpamView,
    UserQuickSearch
)

from django.urls import path



urlpatterns = [
    path("report/", UserQuickSearch.as_view(), name="report_spam"),
]
