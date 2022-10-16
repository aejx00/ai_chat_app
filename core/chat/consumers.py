import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from . import tasks


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room = text_data_json['room_name']


        # Here we can process client data and send result back directly
        # to the client (by using his unique channel name - `self.channel_name`)
        # tasks.add(self.channel_name, message)
        # await self.send(text_data=json.dumps({
        #     'user': 'user', 'message': message, 'bool_flag': False, 'room_name' : room
        # }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_message',
                'message': message,
                'room_name': room,
                'user': 'user'
            }
        )


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'room_name': room
            }
        )



    async def chat_message(self, event):
        # get AI response
        voice, bot_message, bool_check = tasks.respond(event['message'], event['room_name'])
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user': voice,'message': bot_message, 'bool_flag': bool_check
        }))
    
    

    async def user_message(self, event):
        # forward user message
        await self.send(text_data=json.dumps({
            'user': 'user', 'message': event['message'], 'bool_flag': False, 'room_name' : event['room_name']
        }))



    async def send_from_view(self, event):
        print(event)
        await self.send(
            json.dumps({
                'type': 'events.alarm',
                'content': event['content']
            })
        )
    
        