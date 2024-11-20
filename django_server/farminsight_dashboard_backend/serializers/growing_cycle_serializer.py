from rest_framework import serializers
from farminsight_dashboard_backend.models import GrowingCycle


class GrowingCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowingCycle
        fields = [
            'id',
            'startDate',
            'endDate',
            'plants',
            'note',
        ]
