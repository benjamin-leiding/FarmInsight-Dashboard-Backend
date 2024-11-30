from rest_framework import serializers

from django_server import settings
from farminsight_dashboard_backend.models import Camera
from farminsight_dashboard_backend.serializers.snapshot_serializer import SnapshotURLSerializer


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = [
            'id',
            'name',
            'location',
            'modelNr',
            'resolution',
            'isActive',
            'intervalSeconds',
            'livestreamUrl',
            'snapshotUrl',
        ]

    def validate(self, data):
        interval = data.get('intervalSeconds')
        if interval <= 0:
            raise serializers.ValidationError("The interval must be greater than 0.")
        return data

class CameraImageSerializer(serializers.ModelSerializer):
    images = SnapshotURLSerializer(many=True, source='snapshots')

    class Meta:
        model = Camera
        fields = [
            'id',
            'name',
            'location',
            'modelNr',
            'resolution',
            'isActive',
            'intervalSeconds',
            'livestreamUrl',
            'snapshotUrl',
            'images'
        ]

