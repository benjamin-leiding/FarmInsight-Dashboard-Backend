from farminsight_dashboard_backend.serializers import FPFSerializer


def create_fpf(data) -> FPFSerializer:
    """
    Create the FPF in the database and
    create a new bucket in the influxdb
    :param data:
    :return:
    """
    from farminsight_dashboard_backend.services import InfluxDBManager
    serializer = FPFSerializer(data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        InfluxDBManager.get_instance().sync_fpf_buckets()

    return serializer
