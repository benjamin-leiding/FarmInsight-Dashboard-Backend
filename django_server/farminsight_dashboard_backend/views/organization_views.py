from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from farminsight_dashboard_backend.serializers import OrganizationFullSerializer
from farminsight_dashboard_backend.services import create_organization, get_memberships, get_organization_by_id


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def post_organization(request):
    org = create_organization(request.data, request.user)
    return Response(org.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_own_organizations(request):
    memberships = get_memberships(request.user)
    data = []
    for membership in memberships:
        data.append({
            'id': membership.organization.id,
            'name': membership.organization.name,
            'membership': {
                'id': membership.id,
                'role': membership.membershipRole,
            }
        })
    return Response(data)


@api_view(['GET'])
def get_organization(request, organization_id):
    org = get_organization_by_id(organization_id)
    if org is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if len(org.membership_set.filter(userprofile=request.user).all()) == 0: # this Endpoint is only for org members
        return Response(status=status.HTTP_403_FORBIDDEN)

    return Response(OrganizationFullSerializer(org).data)