from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Membership
from ..services import create_organization


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_organization(request):
    org = create_organization(request.data["name"], request.data["isPublic"], request.user)
    data = {
        "id": org.id,
        "name": org.name,
        "isPublic": org.isPublic,
    }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_own_organizations(request):
    memberships = Membership.objects.filter(userprofile_id=request.user.id).prefetch_related('organization').all()
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