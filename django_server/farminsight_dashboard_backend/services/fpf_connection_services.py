from json import JSONDecodeError

import requests
from requests import RequestException



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
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjlFREE4MDY3Qzk0ODFBRkU4QjY1QjNGQThBMjZCRTY3IiwidHlwIjoiYXQrand0In0.eyJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LWlzc2UtaWRlbnRpdHlzZXJ2ZXIuYXp1cmV3ZWJzaXRlcy5uZXQiLCJuYmYiOjE3MzI4OTA0OTgsImlhdCI6MTczMjg5MDQ5OCwiZXhwIjoxNzMyODk0MDk4LCJhdWQiOiJodHRwczovL2RldmVsb3BtZW50LWlzc2UtaWRlbnRpdHlzZXJ2ZXIuYXp1cmV3ZWJzaXRlcy5uZXQvcmVzb3VyY2VzIiwic2NvcGUiOlsib3BlbmlkIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiaW50ZXJhY3RpdmUiLCJzdWIiOiI4NTdlZDZkYy04MGMxLTQ0ZTMtODU1ZC0yYWEzNTFjNTI2ODUiLCJhdXRoX3RpbWUiOjE3MzI2MDMyMTAsImlkcCI6ImxvY2FsIiwiZW1haWwiOiJqLnNjaG9lcGVAb3N0ZmFsaWEuZGUiLCJuYW1lIjoiai5zY2hvZXBlQG9zdGZhbGlhLmRlIiwiaWQiOiI4NTdlZDZkYy04MGMxLTQ0ZTMtODU1ZC0yYWEzNTFjNTI2ODUiLCJzaWQiOiJBM0MyMDQ2Q0Y4MjczMjY4MDUyMEYxREQ5OTVCMDM4QyIsImp0aSI6IkNEOTk4NzcyQ0Q4MjUxQkY4NTFDNEUyQjRGMzM5N0VBIn0.D8yFqnibfeTCdS9CiDxU9Gh2Jw39-IUWohLtwj_JKoAus0hhbSj9NTBw-Pg3gsIzBUedYIEehT1Vq3LkPduQWdjdBdd9svJtoEAyeLLRqoFFbX53-m878SiipXTTF-xm6kxzlONK0tsojpnHodPm9j4Hcv3JxRRzjncpqpioEcmxsroq5QUwoJjPqHzxYpBrmA08UDseKMLJQBJZouLSDzuUTlIUGTPEvZQI2062Of6dOyoAF0lv1_w2VNC-TivGSeyds4x8fdSxcbOuzhPISmEFPhJkxljx8vbQQ3HO3mmsMRGE--azKfuJA4k_KIFBqymwhgvhVAgrb71GCLK7aw'
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
