from django.urls import path

from . import views

app_name = "chats"

urlpatterns = [
        path("", views.index, name="index"),
        path("new/<int:item_id>/", views.new, name="new"),
        path("<int:conversation_id>/", views.chat, name="chat"),
]
