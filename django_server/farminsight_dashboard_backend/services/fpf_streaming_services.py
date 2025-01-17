import cv2
import asyncio

async def http_stream(livestream_url: str):
    """
    Asynchronous generator for streaming frames from an HTTP endpoint.
    """
    camera = cv2.VideoCapture(livestream_url)
    if not camera.isOpened():
        print("Could not open the camera or stream.")
        yield b"Error: Could not open the camera or stream.\r\n"
        return

    try:
        frame_interval = 1 / 30  # Target frame interval for 30 FPS
        while True:
            start_time = asyncio.get_event_loop().time()

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

            # Adjust sleep time based on processing time
            elapsed_time = asyncio.get_event_loop().time() - start_time
            sleep_time = max(0, frame_interval - elapsed_time)
            await asyncio.sleep(sleep_time)
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
        frame_interval = 1 / 30  # Target frame interval for 30 FPS
        while True:
            start_time = asyncio.get_event_loop().time()
            ret, frame = cap.read()
            if not ret:
                break

            _, jpeg = cv2.imencode('.jpg', frame)
            yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            )

            # Adjust sleep time based on processing time
            elapsed_time = asyncio.get_event_loop().time() - start_time
            sleep_time = max(0, frame_interval - elapsed_time)
            await asyncio.sleep(sleep_time)

    finally:
        cap.release()
        print("Camera released.")
