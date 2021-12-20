from django.db import models


class ChatRoom(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Message(models.Model):

    chat_room = models.ForeignKey(ChatRoom,
                                  on_delete=models.CASCADE,
                                  related_name="messages")
    text = models.TextField()

    def __str__(self):
        return self.chat_room
