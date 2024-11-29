from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.models import Camera, FPF


def get_camera_by_id(camera_id):
    try:
        return Camera.objects.get(id=camera_id)
    except Camera.DoesNotExist:
        raise NotFoundException(f'Camera with id: {camera_id} was not found.')


def create_camera(fpf_id, camera_data):
    try:
        fpf = FPF.objects.get(id=fpf_id)
    except FPF.DoesNotExist:
        raise ValueError("FPF with the given ID does not exist")
    camera = Camera.objects.create(FPF=fpf, **camera_data)
    return camera


def update_camera(camera_id, camera_data):
    camera = get_camera_by_id(camera_id)
    for key, value in camera_data.items():
        setattr(camera, key, value)
    camera.save()
    return camera


def delete_camera(camera_id):
    camera = get_camera_by_id(camera_id)
    camera.delete()
    return True