import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def fetch_message(self, data):
        messages = Message.last_30_messages()
        content = {
            'messages': self.messages_to_json(messages)
        }
        self.send_chat_message(content)

    async def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    async def message_to_json(self, message: Message):
        return {
            'author': message.author.get_username(),
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    async def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user, content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message=message)
        }

        return self.send_chat_message(content)

    commands = {
        'fetch_data': fetch_message,
        'new_message': new_message
    }

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
