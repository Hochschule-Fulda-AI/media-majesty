# urls.py
from django.urls import path

from . import views
from . import search_view
from . import approval_view
from . import download_view

app_name = "items"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("<int:id>/", views.item, name="item"),
    path("<int:id>/edit/", views.edit, name="edit"),
    path("<int:id>/delete/", views.delete, name="delete"),
    path("<int:id>/approve/", approval_view.approve_item, name="approve_item"),
    path("pending/", approval_view.pending_items, name="pending_items"),
    path("pending/<int:id>/", approval_view.pending_item, name="pending_item"),
    path(
        "api/search_suggestions/",
        search_view.search_suggestion,
        name="search_suggestion",
    ),
    path("download/<int:id>/", download_view.download, name="download"),
    path("<int:id>/report/", approval_view.report_item, name="report_item"),

]
