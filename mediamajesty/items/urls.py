# urls.py
from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("<int:id>/", views.item, name="item"),
    path("<int:id>/edit/", views.edit, name="edit"),
    path("<int:id>/delete/", views.delete, name="delete"),
    path("api/search_suggestions/", views.search_suggestion, name="search_suggestion"),
]
