import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.notification_kwargs = self.scope['url_route']['kwargs']
        stream = self.notification_kwargs.get('stream', 'default')
        self.notification_group_name = stream
        self.groups.append(self.notification_group_name)
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )


async def notify(self, content, **kwargs):
    sendData = {'type': content['type'], 'message': content['message']}
    await self.send(text_data=json.dumps(sendData))

async def receive(self, text_data, **kwargs):
    self.notification_kwargs = self.scope['url_route']['kwargs']
    stream = self.notification_kwargs.get('stream', 'default')
    self.notification_group_name = stream
    await self.channel_layer.group_send(
        self.notification_group_name,
        {
            'type': 'notify',
            'message': text_data
        }
    )


async def send_notification(self, content):
    channel_layer = get_channel_layer()
    for group_name in content['send_to']:
        await channel_layer.group_send(
            group_name,
            {
                'type': 'notify',
                'mesage': content['message']
            }
        )
