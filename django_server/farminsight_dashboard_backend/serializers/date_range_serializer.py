from rest_framework import serializers

class DateRangeSerializer(serializers.Serializer):
    """
    Accepts format of ISO 8601 (%Y-%m-%dT%H:%M:%SZ) and a simpler YYYY-MM-DD format.
    """
    from_date = serializers.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d'],
        required=False,
        default=None
    )
    to_date = serializers.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d'],
        required=False,
        default=None
    )
