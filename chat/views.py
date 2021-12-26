from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom


@login_required
def chat_view(request, room_name):

    context = {
        'room_name': room_name,
        'username': request.user.username
    }
    return render(request, 'chat.html', context)
