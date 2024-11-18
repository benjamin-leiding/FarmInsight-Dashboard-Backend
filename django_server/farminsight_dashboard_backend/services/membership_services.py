from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied

from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.serializers import MembershipSerializer
from farminsight_dashboard_backend.models import Userprofile, Membership, MembershipRole, SystemRole


def get_memberships(user: Userprofile) -> QuerySet[Membership]:
    return Membership.objects.filter(userprofile_id=user.id).prefetch_related('organization').all()


def create_membership(creating_user: Userprofile, data: dict) -> MembershipSerializer:
    # Check that the one adding a Member is an Admin of the Organization, or System Admin of the Backend
    memberships = get_memberships(creating_user) \
        .filter(organization_id=data['organizationId'], membershipRole=MembershipRole.Admin.value) \
        .all()

    if len(memberships) > 0 or creating_user.systemRole == SystemRole.SystemAdmin.value:
        membership_serializer = MembershipSerializer(data=data)
        if membership_serializer.is_valid(raise_exception=True):
            membership_serializer.save()

        return membership_serializer
    raise PermissionDenied()


def update_membership(membership_id, creating_user, new_membership_role):
    """
    An Admin of the Organization, or System Admin of the Backend
    can promote a user.
    :param membership_id:
    :param creating_user:
    :param new_membership_role:
    :return:
    """

    try:
        membership = Membership.objects.get(id=membership_id)
    except Membership.DoesNotExist:
        raise NotFoundException(f'Membership {membership_id} not found.')

    memberships = get_memberships(creating_user) \
        .filter(organization_id=membership.organization.id, membershipRole=MembershipRole.Admin.value) \
        .all()

    if len(memberships) > 0 or creating_user.systemRole == SystemRole.SystemAdmin.value:
        membership.membershipRole = new_membership_role
        membership.save()
        return
    raise PermissionDenied()


def remove_membership(membership_id, creating_user):
    """
    Only an admin can delete a user.
    :param membership_id:
    :param creating_user:
    :return:
    """
    try:
        membership = Membership.objects.get(id=membership_id)
    except Membership.DoesNotExist:
        raise NotFoundException(f'Membership {membership_id} not found.')

    memberships = get_memberships(creating_user) \
        .filter(organization_id=membership.organization.id, membershipRole=MembershipRole.Admin.value) \
        .all()

    if len(memberships) > 0 or creating_user.systemRole == SystemRole.SystemAdmin.value:
        membership.delete()
        return
    raise PermissionDenied()


def is_member(user, organization_id):
    memberships = get_memberships(user)
    if organization_id not in memberships:
        return False
    return True
