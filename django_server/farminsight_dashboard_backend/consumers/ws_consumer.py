from channels.generic.websocket import WebsocketConsumer
import json


class MeasurementUpdatesConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def send_measurement(self, event):
        measurement = event['measurement']

        self.send(text_data=json.dumps({
            'measurement': measurement
        }))
