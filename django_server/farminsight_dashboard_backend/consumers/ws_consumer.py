import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class SensorUpdatesConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['sensor_id']
        self.room_group_name = f'sensor_updates_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def sensor_measurement(self, event):
        measurement = event['measurement']

        self.send(text_data=json.dumps({
            'measurement': measurement
        }))
