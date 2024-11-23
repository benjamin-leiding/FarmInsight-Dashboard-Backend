from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.models import Sensor
from farminsight_dashboard_backend.serializers.sensor_serializer import SensorSerializer


def get_sensor(sensor_id) -> Sensor:
    """
    Return the sensor by given id populated with additional technical information by the FPF.
    :param sensor_id:
    :return:
    """
    try:
        sensor = Sensor.objects.get(id=sensor_id)
    except Sensor.DoesNotExist:
        raise NotFoundException(f'Sensor {sensor_id} not found.')

    return sensor


def update_sensor(sensor_id, new_sensor):
    """
    Update the sensor by sensor id and a new sensor object
    :param sensor_id:
    :param new_sensor:
    :return:
    """
    try:
        sensor = Sensor.objects.get(id=sensor_id)
    except Sensor.DoesNotExist:
        raise NotFoundException(f"Sensor {sensor_id} not found.")

    serializer = SensorSerializer(sensor, data=new_sensor, partial=True)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return serializer.data


def create_sensor(fpf_id, sensor):
    """
    Send the sensor information to the fpf. On success, create the sensor config in the database
    Create a new Sensor in the database
    :return:
    """
    serializer = SensorSerializer(data=sensor, partial=True)
    if serializer.is_valid(raise_exception=True):
        sensor["fpf_id"] = fpf_id
        serializer.save()

    return sensor
