from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from farminsight_dashboard_backend.services import create_single_use_token


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_websocket_token(request):
    token = create_single_use_token()
    return Response({'token': token}, status=status.HTTP_200_OK)