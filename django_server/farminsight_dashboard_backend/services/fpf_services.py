from farminsight_dashboard_backend.models import FPF, Userprofile
from farminsight_dashboard_backend.serializers import FPFSerializer
from .membership_services import get_memberships


def create_fpf(data) -> FPFSerializer:
    """
    Create the FPF in the database and
    create a new bucket in the influxdb
    :param data:
    :return:
    """
    from farminsight_dashboard_backend.services import InfluxDBManager
    serializer = FPFSerializer(data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        InfluxDBManager.get_instance().sync_fpf_buckets()

    return serializer


def get_fpf_by_id(fpf_id: str):
    fpf = FPF.objects.get(id=fpf_id)
    return fpf


def is_user_part_of_fpf(fpf_id:str, user:Userprofile) -> bool:
    fpf = get_fpf_by_id(fpf_id)

    memberships = get_memberships(user).filter(organization_id=fpf.organization_id).all()
    return len(memberships) > 0