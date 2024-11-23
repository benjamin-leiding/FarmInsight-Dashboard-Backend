import requests
from requests import RequestException
from farminsight_dashboard_backend.services import get_fpf_by_id


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
    fpf = get_fpf_by_id(fpf_id)
    url = f"{build_fpf_url(fpf.get('sensorServiceIp'), endpoint)}"
    try:
        response = requests.request(method, url, json=data, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except RequestException as e:
        raise Exception(f"Cannot reach the FPF service at {url}: {str(e)}")

    except ValueError:
        raise Exception("Invalid JSON response from the FPF service.")


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
