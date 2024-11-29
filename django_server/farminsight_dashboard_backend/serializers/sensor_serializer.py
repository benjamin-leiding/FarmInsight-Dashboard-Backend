from rest_framework import serializers
from farminsight_dashboard_backend.models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = [
            'id',
            'name',
            'location',
            'unit',
            'modelNr',
            'isActive',
            'intervalSeconds',
        ]


class SensorDBSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        extra_kwargs = {
            'additional_fields': {'required': False}
        }
