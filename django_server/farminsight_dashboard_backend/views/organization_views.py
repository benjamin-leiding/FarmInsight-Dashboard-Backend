from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Membership
from ..services.organization_services import create_organization


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_organization(request):
    org = create_organization(request.data["name"], request.data["isPublic"], request.user)
    memberships = Membership.objects.filter(organization=org).prefetch_related('userprofile')
    data = {
        "id": org.id,
        "name": org.name,
        "isPublic": org.isPublic,
        "memberships": [{
            "id": membership.id,
            "role": membership.membershipRole,
            "userprofile": {
                "name": membership.userprofile.name,
            }
        } for membership in memberships]
    }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_own_organizations(request):
    memberships = Membership.objects.filter(userprofile_id=request.user.id).prefetch_related('organization').all()
    orgs = set((membership.organization, membership.membershipRole) for membership in memberships)
    data = []
    for org, role in orgs:
        data.append({
            'id': org.id,
            'name': org.name,
            'isPublic': org.isPublic,
            'membershipRole': role,
        })
    return Response(data)