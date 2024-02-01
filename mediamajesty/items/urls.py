# urls.py
from django.urls import path

from . import approval_view, download_view, search_view, views
from .views import thank_you_view

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
    path("<int:id>/feedback/", views.feedback_form, name="feedback_form"),
    path("feedback/thank_you/", thank_you_view, name="thank_you"),
]
