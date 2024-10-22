from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Membership


@api_view(['GET'])
def get_own_memberships(self, request):
    memberships = Membership.objects.filter(userprofile_id=request.user.id).all()
    return Response(memberships)
