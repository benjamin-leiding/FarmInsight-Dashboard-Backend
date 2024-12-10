from datetime import timedelta

import requests
from channels.db import database_sync_to_async
from decouple import config
from django.utils import timezone

from farminsight_dashboard_backend.models import Sensor, SingleUseToken
from farminsight_dashboard_backend.utils import generate_random_token


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
    if sensor.FPF.apiKeyValidUntil is None:
        return sensor.FPF.apiKey == api_key
    return sensor.FPF.apiKey == api_key and sensor.FPF.apiKeyValidUntil > timezone.now()


def create_single_use_token() -> str:
    token = generate_random_token(length=64)
    SingleUseToken.objects.create(
        token=token,
        valid_until=timezone.now() + timedelta(minutes=1),
    )

    return token


@database_sync_to_async
def check_single_use_token(token_: str):
    SingleUseToken.objects.filter(valid_until__lt=timezone.now()).delete()

    token = SingleUseToken.objects.filter(token=token_).first()
    if token is None:
        return False

    token.delete()
    return True