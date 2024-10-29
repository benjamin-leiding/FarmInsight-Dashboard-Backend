from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..services.fpf_services import create_fpf


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_fpf(request):
    fpf = create_fpf(request.data)
    return Response(fpf.data, status=status.HTTP_201_CREATED)