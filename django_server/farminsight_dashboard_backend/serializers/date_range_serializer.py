from rest_framework import serializers

class DateRangeSerializer(serializers.Serializer):
    """
    Accepts format of ISO 8601 (%Y-%m-%dT%H:%M:%SZ) and a simpler YYYY-MM-DD format.
    """
    from_date = serializers.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d'],
        required=False,
        default=None,
    )

    to_date = serializers.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d'],
        required=False,
        default=None,
    )

    def to_internal_value(self, data):
        """
        Override to map 'from' and 'to' in input data to 'from_date' and 'to_date'.
        """
        data = data.copy()

        if 'from' in data:
            data['from_date'] = data.pop('from')[0]
        if 'to' in data:
            data['to_date'] = data.pop('to')[0]

        return super().to_internal_value(data)
