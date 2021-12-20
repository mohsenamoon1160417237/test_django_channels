from channels.generic.websocket import WebsocketConsumer
import json
import asyncio
from asgiref.sync import async_to_sync
from .models import ChatRoom, Message


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        room = ChatRoom.objects.get_or_create(name=self.room_name)
        self.room = room[0]
        messages = Message.objects.filter(chat_room=self.room)
        msg_list = []
        for x in messages:
            msg_list.append(x.text)
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'load_messages',
                'messages': msg_list
            }
        )

    def disconnect(self, code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):

        data = json.loads(text_data)
        message = data['message']
        Message.objects.create(chat_room=self.room,
                               text=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'new_message',
                'message': message
            }
        )

    def load_messages(self, event):

        messages = event['messages']
        self.send(json.dumps({
            'command': 'messages',
            'messages': messages
        }))

    def new_message(self, event):

        message = event['message']
        self.send(json.dumps({
            'command': 'message',
            'message': message
        }))