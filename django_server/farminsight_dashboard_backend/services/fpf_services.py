from farminsight_dashboard_backend.serializers import FPFSerializer


def create_fpf(data) -> FPFSerializer:
    serializer = FPFSerializer(data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return serializer
