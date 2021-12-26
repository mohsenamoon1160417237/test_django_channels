from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@database_sync_to_async
def get_or_create_chat_room(room_name):
    room = ChatRoom.objects.get_or_create(name=room_name)
    room = room[0]
    return room


@database_sync_to_async
def get_chat_room_mesages(room):
    messages = Message.objects.filter(chat_room=room)
    msg_list = []
    for x in messages:
        msg_list.append(x.text)
    return msg_list


@database_sync_to_async
def create_message(room, text, user):
    Message.objects.create(chat_room=room, text=text, user=user)


@database_sync_to_async
def get_chat_room_users(room):
    return room.users.all()


@database_sync_to_async
def get_user(username):
    return get_object_or_404(User, username=username)


@database_sync_to_async
def get_message_text(msg):
    return msg.text


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room = await get_or_create_chat_room(self.room_name)
        msg_list = await get_chat_room_mesages(self.room)
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'load_messages',
                'messages': msg_list
            }
        )

    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):

        data = json.loads(text_data)
        username = data['username']
        user = await get_user(username)
        message = data['message']
        await create_message(self.room, message, user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'new_message',
                'message': message
            }
        )

    async def load_messages(self, event):

        messages = event['messages']
        await self.send(json.dumps({
            'command': 'messages',
            'messages': messages
        }))

    async def new_message(self, event):

        message = event['message']
        await self.send(json.dumps({
            'command': 'message',
            'message': message
        }))