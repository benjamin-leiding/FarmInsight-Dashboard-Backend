import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from farminsight_dashboard_backend.models import Camera
from farminsight_dashboard_backend.services.fpf_connection_services import fetch_camera_snapshot

logger = logging.getLogger("farminsight_dashboard_backend")

def schedule_camera_snapshots():
    cameras = Camera.objects.filter(isActive=True)
    for camera in cameras:
        interval = camera.intervalSeconds
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            fetch_camera_snapshot,
            trigger=IntervalTrigger(seconds=interval),
            args=[camera.id, camera.snapshotUrl],
            id=f"camera_{camera.id}_snapshot",
            replace_existing=True,
        )
        logger.info(f"Camera {camera.id} snapshot task scheduled for execution with interval {interval}")
        scheduler.start()


def start_scheduler():
    """Initialize the scheduler when the Django server starts."""
    schedule_camera_snapshots()