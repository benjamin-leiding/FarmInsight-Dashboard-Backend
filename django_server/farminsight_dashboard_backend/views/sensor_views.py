from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from farminsight_dashboard_backend.services.sensor_services import get_sensor_types_from_fpf, get_sensor, create_sensor, \
    update_sensor
from farminsight_dashboard_backend.utils import is_valid_uuid


class SensorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        get_sensor()
        return

    def post(self, request):
        """
        Create a new sensor
        :param request:
        :return:
        """
        fpf_id = request.data.get('fpfId')
        sensor = request.data.get('sensor')
        create_sensor(fpf_id, sensor)
        return

    def put(self):
        update_sensor()
        return

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fpf_sensor_types(request, fpf_id):
    """
    Verify that the fpf exists
    try to send a request to the fpf
    :return:
    """
    if is_valid_uuid(fpf_id):
        sensor_types = get_sensor_types_from_fpf(fpf_id)
        return Response(sensor_types, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)