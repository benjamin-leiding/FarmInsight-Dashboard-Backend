from rest_framework.exceptions import PermissionDenied

from farminsight_dashboard_backend.models import Userprofile, GrowingCycle
from farminsight_dashboard_backend.services import is_user_part_of_fpf
from farminsight_dashboard_backend.serializers import GrowingCycleSerializer


def create_growing_cycle(data, creating_user: Userprofile) -> GrowingCycleSerializer:
    if not is_user_part_of_fpf(data['fpfId'], creating_user):
        raise PermissionDenied()

    serializer = GrowingCycleSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer


def update_growing_cycle(growing_cycle_id:str, data, creating_user: Userprofile) -> GrowingCycleSerializer:
    if not is_user_part_of_fpf(data['fpfId'], creating_user):
        raise PermissionDenied()

    growing_cycle = GrowingCycle.objects.get(id=growing_cycle_id)
    serializer = GrowingCycleSerializer(growing_cycle, data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer
