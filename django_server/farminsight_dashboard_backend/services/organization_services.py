from farminsight_dashboard_backend.models import Membership, MembershipRole
from farminsight_dashboard_backend.serializers import OrganizationSerializer


def create_organization(data, user) -> OrganizationSerializer:
    serializer = OrganizationSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        org = serializer.save()
        Membership.objects.create(organization=org, userprofile=user, membershipRole=MembershipRole.Admin.value)
    return serializer
