from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from items.models import Item
from .models import Conversation, Message


@login_required
def index(request):
    user = request.user
    conversations = Conversation.objects.filter(
        Q(buyer=user) | Q(seller=user)
    ).order_by(
        "-created_at"
    )  # todo: update based on last message
    return render(request, "chats/inbox.html", {"conversations": conversations})


@login_required
def chat(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    user = request.user
    partner = conversation.buyer if user == conversation.seller else conversation.seller
    messages = Message.objects.filter(conversation=conversation)[0:10]
    reversed_messages = []
    if messages:
        reversed_messages = reversed(messages) # reverse order to show newest messages at the bottom
        conversation.last_message = messages[0].content
        conversation.save()
    return render(
        request,
        "chats/chat.html",
        {
            "conversation": conversation,
            "user": user,
            "partner": partner,
            "messages": reversed_messages,
        },
    )


@login_required
def new(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    conversation, created = Conversation.objects.get_or_create(
        buyer=request.user, seller=item.created_by, item=item
    )
    return redirect("chats:chat", conversation_id=conversation.id)  # type: ignore
