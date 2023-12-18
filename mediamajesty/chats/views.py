from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from items.models import Item
from .models import Conversation, Message


@login_required
def index(request):
    user = request.user
    conversations = Conversation.objects.filter(Q(buyer=user) | Q(seller=user))
    return render(request, "chats/inbox.html", {"conversations": conversations})


@login_required
def chat(request, conversation_id):
    print(conversation_id)
    converstaion = get_object_or_404(Conversation, pk=conversation_id)
    return render(
        request,
        "chats/chat.html",
        {
            "conversation": converstaion,
            "mesages": [],
        },
    )


@login_required
def new(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    conversation, created = Conversation.objects.get_or_create(
        buyer=request.user, seller=item.created_by, item=item
    )
    return redirect("chats:chat", conversation_id=conversation.id)
