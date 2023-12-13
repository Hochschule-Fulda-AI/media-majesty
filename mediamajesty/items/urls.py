# urls.py
from django.urls import path
from .views import items, SearchSuggestionsView, add_new_item, index, edit_item, delete_item, generate_dummy_posts

app_name = "items"

urlpatterns = [
    path("", items, name="items"),
    path("add/", add_new_item, name="add_new_item"),
    path("<int:id>/", index, name="index"),
    path("<int:id>/edit/", edit_item, name="edit_item"),
    path("<int:id>/delete/", delete_item, name="delete_item"),
    path("generate_dummy_posts/", generate_dummy_posts, name="generate_dummy_posts"),
    path("api/search_suggestions/", SearchSuggestionsView.as_view(), name="search_suggestions"),
]
