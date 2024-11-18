from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.models import FPF
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


def get_fpf_by_id(fpf_id):
    """
    Return FPF by given id
    :param fpf_id:
    :return:
    """
    try:
        sensor = FPF.objects.get(id=fpf_id)
    except FPF.DoesNotExist:
        raise NotFoundException(f'FPF {fpf_id} not found.')
    return sensor


