from canary.views import (
    UserQuickSearch,
    NodeQuickSearch
)

from django.urls import path



urlpatterns = [
    path("search/user/", UserQuickSearch.as_view(), name="search_user"),
    path("search/node/", NodeQuickSearch.as_view(), name="search_node"),
]
