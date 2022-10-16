from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.convo_ai import voices_cleaned


def home(request):
   return redirect('index')


def index(request):
    return render(request, 'chat/index.html', {'voices': voices_cleaned})


def room(request, room_name):
    return render(request, 'chat/room.html', {
            'room_name': room_name
        })


def alarm(req):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('chat_lobbyh', {
    'type': 'send_from_view',
    'content': 'triggered'
    })

    return HttpResponse('<p>Done</p>')