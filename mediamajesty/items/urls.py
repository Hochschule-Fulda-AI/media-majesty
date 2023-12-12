# urls.py
from django.urls import path
from . import views

app_name = "items"

urlpatterns = [
    path("", views.items, name="items"),
    path("add/", views.add_new_item, name="add_new_item"),
    path("<int:id>/", views.index, name="index"),
    path("<int:id>/edit/", views.edit_item, name="edit_item"),
    path("<int:id>/delete/", views.delete_item, name="delete_item"),
    path("generate_dummy_posts/", views.generate_dummy_posts, name="generate_dummy_posts"),  # Add this line
]
