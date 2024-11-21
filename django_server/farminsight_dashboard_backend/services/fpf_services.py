from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.models import FPF
from farminsight_dashboard_backend.serializers import FPFSerializer
from farminsight_dashboard_backend.serializers.fpf_serializer import FPFFullSerializer


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
    fpf = FPF.objects.filter(id=fpf_id).prefetch_related('sensors', 'cameras', 'growingCycles').first()
    if fpf is None:
        raise NotFoundException(f'FPF with id: {fpf_id} was not found.')

    serializer = FPFFullSerializer(instance=fpf)
    return serializer.data
