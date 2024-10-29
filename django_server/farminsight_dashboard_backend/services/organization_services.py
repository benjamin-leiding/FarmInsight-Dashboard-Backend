from farminsight_dashboard_backend.models import Organization, Membership, MembershipRole


def create_organization(name: str, is_public: bool, user) -> Organization:
    org = Organization.objects.create(name=name, isPublic=is_public)
    Membership.objects.create(organization=org, userprofile=user, membershipRole=MembershipRole.Admin.value)
    return org