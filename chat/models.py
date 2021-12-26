from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):

    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(User, related_name="chat_rooms")

    def __str__(self):
        return self.name



class Message(models.Model):

    chat_room = models.ForeignKey(ChatRoom,
                                  on_delete=models.CASCADE,
                                  related_name="messages",
                                  null=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='messages',
                             null=True)
    text = models.TextField()

    def __str__(self):
        return self.chat_room
