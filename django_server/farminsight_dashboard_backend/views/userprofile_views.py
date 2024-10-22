from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Userprofile


@api_view(['GET'])
def get_userprofile(self, request):
    userprofile = Userprofile.objects.filter(id=request.user.id).first()
    return Response(userprofile)
