import uuid
from json import JSONDecodeError
import requests
from django.core.files import File
from requests import RequestException
from farminsight_dashboard_backend.models import Image



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
    token = 'TOKEN'
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
            Image.objects.create(
                camera_id=camera_id,
                image=File(response.raw, name=filename)
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
