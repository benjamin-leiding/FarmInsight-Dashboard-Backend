from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from ..services.fpf_services import create_fpf


@api_view(['POST'])
def post_fpf(request):
    try:
        fpf = create_fpf(
            organization_id=request.data['organizationId'],
            name=request.data['fpf']['name'],
            is_public=request.data['fpf']['isPublic'],
            sensor_service_ip=request.data['fpf']['sensorServiceIp'],
            camera_service_ip=request.data['fpf']['cameraServiceIp'],
            address=request.data['fpf']['address']
        )
    except ValidationError as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'id': fpf.id,
        'name': fpf.name,
        'isPublic': fpf.isPublic,
        'sensorServiceIp': fpf.sensorServiceIp,
        'cameraServiceIp': fpf.cameraServiceIp,
        'address': fpf.address,
        'organization': {
            'id': fpf.organization.id,
            'name': fpf.organization.name,
        }
    }
    return Response(data, status=status.HTTP_201_CREATED)