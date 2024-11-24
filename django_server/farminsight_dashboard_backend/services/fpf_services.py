from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.models import FPF
from farminsight_dashboard_backend.serializers import FPFSerializer
from farminsight_dashboard_backend.utils import generate_random_api_key
import datetime
from django.utils import timezone


def create_fpf(data) -> FPFSerializer:
    """
    First, save fpf to database and create a new bucket in the influxdb.
    Try to send a new apiKey to the FPF.
    Try to send
    :param data:
    :return:
    """
    from farminsight_dashboard_backend.services import InfluxDBManager
    serializer = FPFSerializer(data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        InfluxDBManager.get_instance().sync_fpf_buckets()
        update_fpf_api_key(serializer.data.get('id'))
    return serializer.data


def get_fpf_by_id(fpf_id):
    fpf = FPF.objects.filter(id=fpf_id).prefetch_related('sensors', 'cameras', 'growingCycles').first()
    if fpf is None:
        raise NotFoundException(f'FPF with id: {fpf_id} was not found.')

    return fpf


def update_fpf_api_key(fpf_id):
    """
    Generate a new apiKey and try to send it to the given FPF.
    On success, save the new key and an apiKeyValidUntil in the database.
    :param fpf_id:
    :return:
    """
    from farminsight_dashboard_backend.services import send_request_to_fpf
    key = generate_random_api_key()
    send_request_to_fpf(fpf_id, 'post', '/api/apiKeys', {"fpfId": fpf_id, "apiKey": key})
    fpf = FPF.objects.get(id=fpf_id)
    fpf.apiKey = key
    fpf.apiKeyValidUntil = timezone.now() + datetime.timedelta(days=30)
    fpf.save()
    return


