from rest_framework import serializers
from farminsight_dashboard_backend.models import Camera


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