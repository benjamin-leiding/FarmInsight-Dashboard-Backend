from ..models import Organization, FPF


def create_fpf(organization_id: str, name: str, is_public: str, sensor_service_ip: str, camera_service_ip: str, address: str) -> FPF:
    org = Organization.objects.get(id=organization_id)
    fpf = FPF(
        organization=org,
        name=name,
        isPublic=is_public,
        sensorServiceIp=sensor_service_ip,
        cameraServiceIp=camera_service_ip,
        address=address
    )
    fpf.clean_fields()
    return fpf