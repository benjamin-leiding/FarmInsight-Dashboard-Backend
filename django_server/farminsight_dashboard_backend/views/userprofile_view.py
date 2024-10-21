from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Userprofile

@api_view(['GET'])
def userprofile(request):
    userprofile = Userprofile.objects.filter(user=request.user)
    return Response(userprofile)