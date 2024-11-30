import uuid
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path

import requests
from requests import RequestException

from django_server import settings
from farminsight_dashboard_backend.models.snapshot import Snapshot


def send_request_to_fpf(fpf_id, method, endpoint, data=None, params=None):
    """
    Send an HTTP request and return the JSON response.
    :param endpoint: API endpoint
    :param fpf_id:
    :param method: 'get', 'post', or 'put'
    :param data: Data to send in the case of post/put
    :param params: Parameters to append to the URL
    :return: JSON response data
    """
    from farminsight_dashboard_backend.services import get_fpf_by_id, get_auth_token
    fpf = get_fpf_by_id(fpf_id)
    url = f"{build_fpf_url(fpf.sensorServiceIp, endpoint)}"
    #token = get_auth_token()
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjlFREE4MDY3Qzk0ODFBRkU4QjY1QjNGQThBMjZCRTY3IiwidHlwIjoiYXQrand0In0.eyJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LWlzc2UtaWRlbnRpdHlzZXJ2ZXIuYXp1cmV3ZWJzaXRlcy5uZXQiLCJuYmYiOjE3MzI4MTYxNjYsImlhdCI6MTczMjgxNjE2NiwiZXhwIjoxNzMyODE5NzY2LCJhdWQiOiJodHRwczovL2RldmVsb3BtZW50LWlzc2UtaWRlbnRpdHlzZXJ2ZXIuYXp1cmV3ZWJzaXRlcy5uZXQvcmVzb3VyY2VzIiwic2NvcGUiOlsib3BlbmlkIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiaW50ZXJhY3RpdmUiLCJzdWIiOiI4NTdlZDZkYy04MGMxLTQ0ZTMtODU1ZC0yYWEzNTFjNTI2ODUiLCJhdXRoX3RpbWUiOjE3MzI2MDMyMTAsImlkcCI6ImxvY2FsIiwiZW1haWwiOiJqLnNjaG9lcGVAb3N0ZmFsaWEuZGUiLCJuYW1lIjoiai5zY2hvZXBlQG9zdGZhbGlhLmRlIiwiaWQiOiI4NTdlZDZkYy04MGMxLTQ0ZTMtODU1ZC0yYWEzNTFjNTI2ODUiLCJzaWQiOiJBM0MyMDQ2Q0Y4MjczMjY4MDUyMEYxREQ5OTVCMDM4QyIsImp0aSI6IkQyN0UwNkZEM0ZDMUI3NzNENTQzNjhFRDc5MTE1NDFFIn0.Q0UsAaZhGAWyjHYDAxnY5rO954hhdgoRTAdXh5CEP0KHj7gRLXmXtq6M6pnjhG4dIdSLSvmsYquikr_k_nZTts7lo8bSS25r1IxpCY3jTTGp4vYqIWaChjtVP_l5qAqXYUqiMpGEdD_CGtPLl09HJz9CfhD21uRlRKUIMldOPOzG49P9FaG7wkl0HY-PCCLix_kl8jdnMNQwVzhW-Ne7eOM0c5VW1IYKl8omggvBR6TezOKC_OJ32JhnuxSbY2g785iyf5MjqXHnKUlhnDV2XSJN72Pm_n2vgukuBq-mRgQOwmbdbLKQydihGJYxlrtevZ6I5jYnwitwXkMfVLRW2A'
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request(method, url, json=data, params=params, headers=headers, timeout=10)
        #response = requests.request(method, url, json=data, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except JSONDecodeError as e:
        return None
    except RequestException as e:
        raise Exception(f"Cannot reach the FPF service at {url}: {str(e)}")

    except ValueError:
        raise Exception("Invalid JSON response from the FPF service.")

def fetch_camera_snapshot(camera_id, snapshot_url):
    """
    Fetch a snapshot from the given snapshot URL of the camera and store it as a jpg file.
    :param camera_id:
    :param snapshot_url:
    :return:
    """
    try:
        response = requests.get(snapshot_url, stream=True)
        if response.status_code == 200:

            filename = f"{str(uuid.uuid4())}.jpg"
            save_path = Path(settings.MEDIA_ROOT) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, "wb") as img_file:
                for chunk in response.iter_content(chunk_size=8192):
                    img_file.write(chunk)

            Snapshot.objects.create(
                camera_id=camera_id,
                file_name=filename
            )

            return filename
        else:
            raise ValueError(f"Failed to fetch snapshot. HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching snapshot for Camera {camera_id}: {e}")

def build_fpf_url(fpf_address, endpoint):
    """
    Build a correct URL based on the FPF config
    :param endpoint:
    :param fpf_address:
    :return:
    """
    if fpf_address.startswith(('http://', 'https://')):
        if endpoint.startswith('/'):
            return f"{fpf_address}{endpoint}"
        return f"{fpf_address}/{endpoint}"
    if endpoint.startswith('/'):
        return f"http://{fpf_address}{endpoint}"
    return f"http://{fpf_address}/{endpoint}"
