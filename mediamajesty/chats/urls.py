from django.urls import path

from . import views

app_name = "chats"

urlpatterns = [
        path("", views.index, name="index"),
        path("chat/<int:conversation_id>", views.chat, name="chat"),
        path("new/<int:item_id>", views.new, name="new"),
]
