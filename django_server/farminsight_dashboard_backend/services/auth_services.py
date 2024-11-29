

import requests
from decouple import config
from django.utils import timezone

from farminsight_dashboard_backend.models import Sensor


def get_auth_token():
    """
    Fetch the authentication token from the external auth service.
    """

    # Safely load sensitive data
    AUTH_SERVICE_URL = config('AUTH_SERVICE_URL')
    AUTH_USERNAME = config('AUTH_USERNAME')
    AUTH_PASSWORD = config('AUTH_PASSWORD')

    try:
        response = requests.post(
            AUTH_SERVICE_URL,
            json={"username": AUTH_USERNAME, "password": AUTH_PASSWORD},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get('token')

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch auth token: {str(e)}")


def valid_api_key_for_sensor(api_key: str, sensor_id: str) -> bool:
    sensor = Sensor.objects.get(id=sensor_id)
    return sensor.FPF.apiKey == api_key and sensor.FPF.apiKeyValidUntil > timezone.now()
