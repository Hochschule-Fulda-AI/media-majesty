from django.urls import path
from . import views

app_name = "items"

urlpatterns = [
        path("<int:id>/", views.index, name="index"),
        path("add/", views.add_new_item, name="add_new_item"),
]
