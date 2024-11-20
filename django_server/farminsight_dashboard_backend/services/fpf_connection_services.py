import requests
from requests import RequestException

from farminsight_dashboard_backend.services import get_fpf_by_id


def get_sensor_types_from_fpf(fpf_id):
    """
    Send GET request to FPF to get the available sensor types
    :param fpf_id:
    :return:
    """
    fpf = get_fpf_by_id(fpf_id)
    url = f"{build_fpf_url(fpf.sensorServiceIp)}/api/sensors/types/available"

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


def get_sensor_from_fpf(fpf_id, sensor_id):
    """
    Request the additional technical sensor information
    :param fpf_id:
    :param sensor_id:
    :return:
    """
    fpf = get_fpf_by_id(fpf_id)
    url = f"{build_fpf_url(fpf.sensorServiceIp)}/api/sensors/{sensor_id}"

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


def create_sensor_at_fpf(fpf_id, fpf_sensor_config):
    """
    Send POST request to FPF to create a new sensor
    :param fpf_sensor_config:
    :param fpf_id:
    :return:
    """
    fpf = get_fpf_by_id(fpf_id)
    url = f"{build_fpf_url(fpf.sensorServiceIp)}/api/sensors"

    try:
        response = requests.post(url, fpf_sensor_config, timeout=10)
        response.raise_for_status()

    except RequestException as e:
        raise Exception(f"Cannot reach FPF sensor service at {url}: {str(e)}")

    try:
        data = response.json()

    except ValueError:
        raise Exception("Invalid JSON response from FPF sensor service.")

    return data


def update_sensor_at_fpf(sensor_id, fpf_id, payload):
    """
    Send the update via PUT request to the fpf
    :param fpf_id:
    :return:
    """
    fpf = get_fpf_by_id(fpf_id)
    url = f"{build_fpf_url(fpf.sensorServiceIp)}/api/sensors/{sensor_id}"

    try:
        response = requests.post(url, fpf_sensor_config, timeout=10)
        response.raise_for_status()

    except RequestException as e:
        raise Exception(f"Cannot reach FPF sensor service at {url}: {str(e)}")

    try:
        data = response.json()

    except ValueError:
        raise Exception("Invalid JSON response from FPF sensor service.")

    return data


def build_fpf_url(fpf_address):
    """
    Build a correct URL based on the FPF config
    :param fpf_address:
    :return:
    """
    if fpf_address.startswith(('http://', 'https://')):
        return fpf_address
    return f"http://{fpf_address}"
