"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from web.views.index_views import (
    index,
    OSFOauthCallbackView,
    OSFOauthView,
)

from web.views.schema_editor.schema_editor import (
    SchemaCreateView,
    SchemaDeleteView,
    SchemaUpdateView,
    BlockCreateView,
    SchemaEditorView,
    BlockDeleteView,
    BlockUpdateView,
    SimpleSchemaJSONView,
    SchemaJSONView,
    BlockEditorView,
    CSVtoSchemaView,
    SchemaCompareView
)
from web.views.bulk_upload_contrbutors.bulk_upload_contributors import (
    BulkUploadContributors,
)

from django.conf.urls import url, include
from django.urls import path


urlpatterns = [
    url(r"^$", index, name="home"),
    url("^", include("django.contrib.auth.urls")),
    url(r"^spam_report/", include('canary.urls')),
    url(r"^admin/", admin.site.urls, name="admin_app"),
    url(r"^osf_oauth/$", OSFOauthView.as_view(), name="osf_oauth"),
    url(r"^callback/$", OSFOauthCallbackView.as_view(), name="callback"),
    url(r"^(?P<schema_id>\w+)/json/$", SchemaJSONView.as_view(), name="schema_json"),
    url(
        r"^(?P<schema_id>\w+)/json/atomicschema/$",
        SimpleSchemaJSONView.as_view(),
        name="atomic_schema",
    ),
    url(r"^schema_editor/", SchemaEditorView.as_view(), name="schema_editor"),
    path("schema/<int:schema_id>/", SchemaUpdateView.as_view(), name="schema-update"),
    path("schema/add/", SchemaCreateView.as_view(), name="schema_add"),
    path(
        "schema/<int:schema_id>/delete/",
        SchemaDeleteView.as_view(),
        name="schema-delete",
    ),
    path(
        "schema/<int:schema_id>/block_editor/",
        BlockEditorView.as_view(),
        name="block_editor",
    ),
    path(
        "schema/csv_to_schema/",
        CSVtoSchemaView.as_view(),
        name="csv_to_schema",
    ),
    path(
        "schema/<int:schema_id>/blocks/<int:block_id>/",
        BlockUpdateView.as_view(),
        name="block-update",
    ),
    path(
        "schema/<int:schema_id>/blocks/add/",
        BlockCreateView.as_view(),
        name="block-add",
    ),
    path(
        "schema/<int:schema_id>/blocks/<int:block_id>/delete/",
        BlockDeleteView.as_view(),
        name="block-delete",
    ),
    url(
        r"^bulk_upload_contributors/$",
        BulkUploadContributors.as_view(),
        name="bulk_upload_contributors",
    ),
    path(r"schema/<int:schema_id>/compare/", SchemaCompareView.as_view(), name='compare'),

]
