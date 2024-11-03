from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied

from farminsight_dashboard_backend.serializers import MembershipSerializer
from farminsight_dashboard_backend.models import Userprofile, Membership, MembershipRole, SystemRole


def get_memberships(user: Userprofile) -> QuerySet[Membership]:
    return Membership.objects.filter(userprofile_id=user.id).prefetch_related('organization').all()


def create_membership(creating_user: Userprofile, data: dict) -> MembershipSerializer:
    # Check that the one adding a Member is an Admin of the Organization, or System Admin of the Backend
    memberships = get_memberships(creating_user)\
        .filter(organization_id=data['organizationId'], membershipRole=MembershipRole.Admin.value)\
        .all()

    if len(memberships) > 0 or creating_user.systemRole == SystemRole.SystemAdmin.value:
        membership_serializer = MembershipSerializer(data=data)
        if membership_serializer.is_valid(raise_exception=True):
            membership_serializer.save()

        return membership_serializer
    raise PermissionDenied()
