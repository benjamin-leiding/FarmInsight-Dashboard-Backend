import logging
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from farminsight_dashboard_backend.models import Camera
from farminsight_dashboard_backend.services.fpf_connection_services import fetch_camera_snapshot

class CameraScheduler:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def __new__(cls, *args, **kwargs):
        return super(CameraScheduler, cls).__new__(cls)

    def __init__(self):
        """
        Initialize the CameraScheduler
        """
        if not getattr(self, "_initialized", False):
            self._scheduler = BackgroundScheduler()
            self.log = logging.getLogger("farminsight_dashboard_backend")
            self._initialized = True

    def start(self):
        """
        Start the scheduler
        :return:
        """
        self._add_all_camera_jobs()
        self._scheduler.start()

        self.log.info("CameraScheduler started.")

    def add_camera_job(self, camera_id: str):
        """
        Add a snapshot task for a specific camera.
        :param camera_id: ID of the camera
        """
        try:
            camera = Camera.objects.get(id=camera_id, isActive=True)
            interval = camera.intervalSeconds
            self._scheduler.add_job(
                fetch_camera_snapshot,
                trigger=IntervalTrigger(seconds=interval),
                args=[camera.id, camera.snapshotUrl],
                id=f"camera_{camera.id}_snapshot",
                replace_existing=True,
            )
            self.log.info(f"Camera {camera.id} snapshot task scheduled with interval {interval} seconds.")
        except Camera.DoesNotExist:
            self.log.warning(f"Camera with ID {camera_id} does not exist or is not active.")

    def remove_camera_job(self, camera_id: str):
        """
        Remove a snapshot task for a specific camera.
        :param camera_id:
        :return:
        """
        try:
            camera = Camera.objects.get(id=camera_id, isActive=True)
            self._scheduler.remove_job(job_id=f"camera_{camera.id}_snapshot")
            self.log.info(f"Camera {camera.id} snapshot task deleted.")
        except Camera.DoesNotExist:
            self.log.warning(f"Camera with ID {camera_id} does not exist or is not active.")

    def _add_all_camera_jobs(self):
        """
        Add snapshot tasks for all active cameras.
        """
        cameras = Camera.objects.filter(isActive=True)
        for camera in cameras:
            self.add_camera_job(str(camera.id))
