from farminsight_dashboard_backend.models import FPF, Sensor
from farminsight_dashboard_backend.utils import get_date_range
from .influx_services import InfluxDBManager
from ..exceptions import NotFoundException


def get_all_fpf_data(fpfId, from_date=None, to_date=None):
    """
    Returns all related data (Sensors, Cameras, GrowingCycles) including measurements and images
    for the given FPF from the databases.
    :param to_date: must be in ISO 8601 format (e.g. 2024-10-01T00:00:00Z) or YYYY-MM-DD format.
    :param from_date: must be in ISO 8601 format (e.g. 2024-10-31T23:59:59Z) or YYYY-MM-DD format.
    :param fpfId: UUID of the FPF
    :return:
    """
    try:
        fpf = FPF.objects.prefetch_related('sensors', 'cameras', 'growingCycles').get(id=fpfId)
    except FPF.DoesNotExist:
        raise NotFoundException(f'FPF with id: {fpfId} was not found.')

    # Set dates and convert to iso code
    from_date_iso, to_date_iso = get_date_range(from_date, to_date)

    fpf_data = {
        "id": str(fpf.id),
        "name": fpf.name,
        "isPublic": fpf.isPublic,
        "sensorServiceIp": fpf.sensorServiceIp,
        "cameraServiceIp": fpf.cameraServiceIp,
        "address": fpf.address,
        'sensors': [],
        "cameras": list(
            fpf.cameras.values('id', 'name', 'location', 'modelNr', 'resolution', 'isActive', 'intervalSeconds')),
        'growingCycles': list(fpf.growingCycles.values('id', 'startDate', 'endDate', 'plants', 'note'))
    }

    # Collect all sensor IDs for InfluxDB query
    sensor_ids = [str(sensor.id) for sensor in fpf.sensors.all()]

    # Fetch measurements for all sensors in one call
    measurements_by_sensor = InfluxDBManager.get_instance().fetch_sensor_measurements(
        fpf_id=fpf.id,
        sensor_ids=sensor_ids,
        from_date=from_date_iso,
        to_date=to_date_iso)

    # Build sensors data with measurements included
    for sensor in fpf.sensors.all():
        sensor_data = {
            "id": str(sensor.id),
            "name": sensor.name,
            "location": sensor.location,
            "unit": sensor.unit,
            "modelNr": sensor.modelNr,
            "isActive": sensor.isActive,
            "intervalSeconds": sensor.intervalSeconds,
            "measurements": measurements_by_sensor.get(str(sensor.id), [])
        }
        fpf_data["sensors"].append(sensor_data)

    return fpf_data


def get_all_sensor_data(sensorId, from_date=None, to_date=None):
    """
    Returns all related data (Sensors, Cameras, GrowingCycles) including measurements and images
    for the given FPF from the databases.
    :param sensorId: UUID of the sensor
    :param to_date: must be in ISO 8601 format (e.g. 2024-10-01T00:00:00Z) or YYYY-MM-DD format.
    :param from_date: must be in ISO 8601 format (e.g. 2024-10-31T23:59:59Z) or YYYY-MM-DD format.
    :return:
    """
    try:
        sensor = Sensor.objects.get(id=sensorId)
    except Sensor.DoesNotExist:
        raise NotFoundException(f'Sensor with id: {sensorId} was not found.')

    # Set dates and convert to iso code
    from_date_iso, to_date_iso = get_date_range(from_date, to_date)

    # Fetch measurements for all sensors in one call
    measurements_by_sensor = InfluxDBManager.get_instance().fetch_sensor_measurements(
        fpf_id=str(sensor.FPF.id),
        sensor_ids=[str(sensor.id)],
        from_date=from_date_iso,
        to_date=to_date_iso)

    return measurements_by_sensor.get(str(sensor.id), [])
