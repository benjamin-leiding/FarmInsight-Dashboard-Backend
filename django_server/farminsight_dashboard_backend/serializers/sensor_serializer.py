from rest_framework import serializers

class SensorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    unit = serializers.CharField(max_length=10)
    modelNr = serializers.CharField(max_length=255)
    isActive = serializers.BooleanField()
    intervalSeconds = serializers.IntegerField(min_value=0)

    def validate_intervalSeconds(self, value):
        if value < 0:
            raise serializers.ValidationError("Interval seconds must be a non-negative value.")
        return value
