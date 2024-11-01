from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from farminsight_dashboard_backend.serializers import UserprofileSerializer
from farminsight_dashboard_backend.services import search_userprofiles


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userprofile(request):
    return Response(UserprofileSerializer(request.user).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userprofile_by_search_string(request, search_string: str):
    userprofiles = search_userprofiles(search_string)[:10]
    return Response(UserprofileSerializer(userprofiles, many=True).data)
