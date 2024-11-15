from django.contrib.sites import requests
from requests import RequestException

from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.models import FPF
from farminsight_dashboard_backend.serializers.sensor_serializer import SensorSerializer


def get_sensor_types_from_fpf(fpf_id):
    """
    Forward the request to the FPF and return the response body
    :param fpf_id:
    :return:
    """
    try:
        fpf = FPF.objects.get(id=fpf_id)
    except FPF.DoesNotExist:
        raise NotFoundException(f'Membership {fpf_id} not found.')

    url = f"{fpf.sensorServiceIp}/api/sensors/types/available"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    except RequestException as e:
        raise Exception(f"Cannot reach FPF sensor service at {url}: {str(e)}")

    try:
        data = response.json()

    except ValueError:
        raise Exception("Invalid JSON response from FPF sensor service.")

    return data

def get_sensor():
    return

def update_sensor():
    return

def create_sensor(fpf_id, sensor):
    """
    Create a new Sensor in the database
    :return:
    """
    try:
        fpf = FPF.objects.get(id=fpf_id)
    except FPF.DoesNotExist:
        raise NotFoundException(f'FPF with id: {fpf_id} was not found.')

    serializer = SensorSerializer(data=sensor, partial=True)
    if serializer.is_valid(raise_exception=True):
        sensor["fpf_id"] = fpf.id
        serializer.save()

    return sensor