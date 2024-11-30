from farminsight_dashboard_backend.models.snapshot import Snapshot


def get_snapshots_by_camera(camera_id, from_date, to_date=None):
    """
    Retrieve snapshots for a specific camera within a given timeframe.

    :param camera_id: ID of the camera
    :param from_date: Start of the date range
    :param to_date: End of the date range (optional, defaults to now)
    :return: Queryset of Snapshot objects within the timeframe
    """
    snapshots = Snapshot.objects.filter(camera_id=camera_id, created_at__gte=from_date)
    if to_date:
        snapshots = snapshots.filter(created_at__lte=to_date)
    return snapshots.order_by('-created_at')
