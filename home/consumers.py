import json
from channels.db import database_sync_to_async
from .models import ChatMessage
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        if self.user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


        join_message = f"{self.user.email} has joined the chat"
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': join_message,
                'user': 'System',  
            }
        )

        messages = await self.get_chat_messages(self.room_name)
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['message'],
                'user': message['user__email'],
            }))

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            await self.save_chat_message(self.user, self.room_name, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.email,
                }
            )
        except Exception as e:
            print(f"Error in receive: {e}")

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    @database_sync_to_async
    def get_chat_messages(self, room_name):
        return list(ChatMessage.objects.filter(room_name=room_name).values('message', 'user__email'))

    @database_sync_to_async
    def save_chat_message(self, user, room_name, message):
        return ChatMessage.objects.create(user=user, room_name=room_name, message=message)