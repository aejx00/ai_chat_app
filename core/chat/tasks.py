# chat/tasks.py

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task
from . import convo_ai

channel_layer = get_channel_layer()

@shared_task
def respond(user_input, voice_input):
    """Process user message and return AI response"""
    if '_' in voice_input:
        voice_input = voice_input.replace('_','-')
    model_result = convo_ai.get_model_response(user_input)
    voice_update = convo_ai.bot_response(voice_input, model_result)
    channel_layer.group_send('bleh', {'type': 'bot_resp', 'message': model_result, 'bool_flag': voice_update})
    return voice_input, model_result, voice_update