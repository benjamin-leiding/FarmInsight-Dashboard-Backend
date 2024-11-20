from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.models import FPF
from farminsight_dashboard_backend.serializers import FPFSerializer


def create_fpf(data) -> FPFSerializer:
    serializer = FPFSerializer(data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return serializer


def get_fpf_by_id(fpf_id):
    fpf = FPF.objects.filter(id=fpf_id).prefetch_related('sensors', 'cameras', 'growingCycles').first()
    if fpf is None:
        raise NotFoundException(f'FPF with id: {fpf_id} was not found.')

    fpf_data = {
        "id": fpf_id,
        "name": fpf.name,
        "isPublic": fpf.isPublic,
        "sensorServiceIp": fpf.sensorServiceIp,
        "cameraServiceIp": fpf.cameraServiceIp,
        "address": fpf.address,
        'Sensors': list(fpf.sensors.values('id', 'name', 'location', 'unit', 'modelNr', 'isActive', 'intervalSeconds')),
        "Cameras": list(
            fpf.cameras.values('id', 'name', 'location', 'modelNr', 'resolution', 'isActive', 'intervalSeconds')),
        'GrowingCycles': list(fpf.growingCycles.values('id', 'startDate', 'endDate', 'plants', 'note'))
    }
    return fpf_data
