from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from farminsight_dashboard_backend.serializers import UserprofileSerializer
from farminsight_dashboard_backend.services import search_userprofiles, update_userprofile_name
from rest_framework.decorators import api_view, permission_classes


class UserprofileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, identifier: str):
        userprofiles = search_userprofiles(identifier)[:10]
        return Response(UserprofileSerializer(userprofiles, many=True).data)

    def put(self, request, identifier):
        updated_userprofile = update_userprofile_name(identifier, request.data.get('name'))
        return Response(UserprofileSerializer(updated_userprofile).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userprofile(request):
    return Response(UserprofileSerializer(request.user).data)
