import cv2
import asyncio

async def http_stream(livestream_url:str):
    """
     Asynchronous generator for streaming frames from http endpoint.
     """
    camera = cv2.VideoCapture(livestream_url)
    if not camera.isOpened():
        print("Could not open the camera or stream.")
        yield b"Error: Could not open the camera or stream.\r\n"
        return

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Failed to grab frame.")
                break

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Failed to encode frame.")
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

            # Async sleep for frame rate control
            await asyncio.sleep(0.1)
    finally:
        camera.release()
        print("Camera released.")


async def rtsp_stream(livestream_url:str):
    """
     Asynchronous generator for streaming frames from rtsp endpoint.
     """
    cap = cv2.VideoCapture(livestream_url)
    if not cap.isOpened():
        yield b"Error: Unable to open RTSP stream."
        return
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, jpeg = cv2.imencode('.jpg', frame)
            yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            )
            await asyncio.sleep(0.1)

    finally:
        cap.release()
        print("Camera released.")
