import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from chats.models import Conversation, Message


# todo: remove type: ignore after fixes
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # type: ignore
        await self.accept()

    async def disconnect(self, _):  # type: ignore
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)  # type: ignore

    # receive message from websocket
    async def receive(self, text_data):  # type: ignore
        data = json.loads(text_data)
        room = data["room"]
        sender = data["sender"]
        message = data["message"]

        # save message to db
        await self.save_message(room, sender, message)

        # send message to room group
        await self.channel_layer.group_send(  # type: ignore
            self.room_group_name,
            {
                "type": "chat.message",
                "room": room,
                "sender": sender,
                "message": message,
            },
        )

    # receive message from room group
    async def chat_message(self, event):
        # send message to websocket
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def save_message(self, room, sender, message):
        sender = User.objects.get(username=sender)
        conversation = Conversation.objects.get(id=room)
        Message.objects.create(
            sender=sender, conversation=conversation, content=message
        )
