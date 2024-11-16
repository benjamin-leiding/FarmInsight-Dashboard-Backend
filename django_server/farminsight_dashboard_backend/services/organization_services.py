from farminsight_dashboard_backend.models import Membership, MembershipRole
from farminsight_dashboard_backend.serializers import OrganizationSerializer
from farminsight_dashboard_backend.models import Organization

def create_organization(data, user) -> OrganizationSerializer:
    serializer = OrganizationSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        org = serializer.save()
        Membership.objects.create(organization=org, userprofile=user, membershipRole=MembershipRole.Admin.value)
    return serializer


def get_organization_by_name(name: str) -> Organization:
    org = Organization.objects.filter(name=name).prefetch_related('membership_set', 'membership_set__userprofile', 'fpf_set').first()
    return org

def get_organization_by_id(id: str) -> Organization:
    org = Organization.objects.filter(id=id).prefetch_related('membership_set', 'membership_set__userprofile', 'fpf_set').first()
    return org