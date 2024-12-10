import cv2
import requests


def http_stream(livestream_url:str):
    try:
        with requests.get(livestream_url, stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
    except requests.exceptions.RequestException as e:
        yield f"Error fetching the HTTP stream: {str(e)}".encode("utf-8")




def rtsp_stream(livestream_url:str):
    cap = cv2.VideoCapture(livestream_url)
    if not cap.isOpened():
        yield b"Error: Unable to open RTSP stream."
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame as JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
        )

    cap.release()


