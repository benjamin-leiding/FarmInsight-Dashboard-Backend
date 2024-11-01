from farminsight_dashboard_backend.models import FPF, Sensor
from farminsight_dashboard_backend.utils import get_date_range
from farminsight_dashboard_backend.utils.influx_data_query_utils import fetch_sensor_measurements


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
        return {'data': {'error': f'FPF with id: {fpfId} not found.'}, 'status': 404}

    # Set dates and convert to iso code
    from_date_iso, to_date_iso = get_date_range(from_date, to_date)

    fpf_data = {
        "id": str(fpf.id),
        "name": fpf.name,
        "isPublic": fpf.isPublic,
        "sensorServiceIp": fpf.sensorServiceIp,
        "cameraServiceIp": fpf.cameraServiceIp,
        "address": fpf.address,
        'sensors' : [],
        "cameras": list(fpf.cameras.values('id', 'name', 'location', 'modelNr', 'resolution', 'isActive', 'intervalSeconds')),
        'growingCycles' : list(fpf.growingCycles.values('id', 'startDate', 'endDate', 'plants', 'note'))
    }

    # Collect all sensor IDs for InfluxDB query
    sensor_ids = [str(sensor.id) for sensor in fpf.sensors.all()]

    # Fetch measurements for all sensors in one call
    measurements_by_sensor = fetch_sensor_measurements(fpf_id=fpf.id,
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

    return {'data': fpf_data, 'status': 200}

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
    except FPF.DoesNotExist:
        return {'data': {'error': f'FPF with id: {sensorId} not found.'}, 'status': 404}

    # Set dates and convert to iso code
    from_date_iso, to_date_iso = get_date_range(from_date, to_date)

        # Fetch measurements for all sensors in one call
    measurements_by_sensor = fetch_sensor_measurements(fpf_id=str(sensor.FPF.id),
                                                       sensor_ids=[str(sensor.id)],
                                                       from_date=from_date_iso,
                                                       to_date=to_date_iso)

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

    return {'data': sensor_data, 'status': 200}