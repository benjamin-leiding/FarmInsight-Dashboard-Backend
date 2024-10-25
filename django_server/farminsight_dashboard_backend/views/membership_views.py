from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Membership


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_own_memberships(request):
    memberships = Membership.objects.filter(userprofile_id=request.user.id).all()
    return Response(memberships)
