from django.shortcuts import render

def chat_view(request, room_name):

    context = {
        'room_name': room_name
    }
    return render(request, 'chat.html', context)
