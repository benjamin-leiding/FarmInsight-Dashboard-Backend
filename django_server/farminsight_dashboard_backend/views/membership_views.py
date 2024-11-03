from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from farminsight_dashboard_backend.services import create_membership


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_membership(request):
    membership_serializer = create_membership(request.user, request.data)
    return Response(membership_serializer.data, status=status.HTTP_201_CREATED)
