from django.urls import path

from chat.consumers import ChatConsumer
from rand_int.consumers import IntConsumer

ws_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
    path("ws/int/", IntConsumer.as_asgi()),
]
