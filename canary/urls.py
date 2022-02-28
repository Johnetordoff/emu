from canary.views import (
    UserQuickSearch
)

from django.urls import path



urlpatterns = [
    path("report/", UserQuickSearch.as_view(), name="report_spam"),
]
