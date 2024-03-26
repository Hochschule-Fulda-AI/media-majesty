from django.contrib.auth.models import User
from django.db import models
from items.models import Item


class Conversation(models.Model):
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer_conversations"
    )
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller_conversations"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="item_conversations"
    )
    last_message = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name}: {self.buyer.username} - {self.seller.username}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:  # type: ignore
        ordering = ("-created_at",)
