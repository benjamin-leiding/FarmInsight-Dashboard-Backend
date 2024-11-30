from rest_framework import serializers
from django.conf import settings

from farminsight_dashboard_backend.models import Snapshot


class SnapshotURLSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Snapshot
        fields = [
            'url',
            'created_at',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        if not request:
            raise ValueError("Request context is not available in the serializer.")
        return f"{request.build_absolute_uri(settings.MEDIA_URL)}{obj.file_name}"