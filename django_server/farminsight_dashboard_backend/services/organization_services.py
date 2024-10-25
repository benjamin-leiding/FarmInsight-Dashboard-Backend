from ..models import Organization, Membership

def create_organization(name: str, is_public: bool, user) -> Organization:
    org = Organization.objects.create(name=name, isPublic=is_public)
    Membership.objects.create(organization=org, userprofile=user, membershipRole='owner')
    return org