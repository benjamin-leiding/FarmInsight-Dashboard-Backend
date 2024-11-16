from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from farminsight_dashboard_backend.services import create_growing_cycle, update_growing_cycle


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_growing_cycle(request):
    growing_cycle = create_growing_cycle(request.data, request.user)
    return Response(growing_cycle.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_growing_cycle(request, growing_cycle_id):
    growing_cycle = update_growing_cycle(growing_cycle_id, request.data, request.user)
    return Response(growing_cycle.data, status=status.HTTP_200_OK)
