from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import FPF, Organization

@api_view(['POST'])
def post_fpf(self, request):
    fpf = FPF.objects.create(
        organization_id=request.data['organizationId'],
        name=request.data['fpf.name'],
        isPublic=request.data['fpf.isPublic'],
        sensorServiceIp=request.data['fpf.sensorServiceIp'],
        cameraServiceIp=request.data['fpf.cameraServiceIp'],
        address=request.data['fpf.address']
    )
    fpf.save()
    return Response(fpf, status=status.HTTP_201_CREATED)