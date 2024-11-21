from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from farminsight_dashboard_backend.serializers import SensorSerializer
from farminsight_dashboard_backend.services import create_sensor_at_fpf, get_memberships, get_organization_by_fpf_id, \
    is_member, get_sensor_types_from_fpf, update_sensor_at_fpf, get_sensor_from_fpf
from farminsight_dashboard_backend.services.sensor_services import get_sensor, create_sensor, \
    update_sensor
from farminsight_dashboard_backend.utils import is_valid_uuid
import uuid


class SensorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, sensor_id):
        """
        Return the sensor by its id.
        Requesting user must be part of the organization.
        :param request:
        :param sensor_id:
        :return:
        """

        if not is_valid_uuid(sensor_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sensor = get_sensor(sensor_id)

        if not is_member(request.user, get_organization_by_fpf_id(sensor.FPF_id).id):
            return Response(status=status.HTTP_403_FORBIDDEN)

        fpf_sensor_info = get_sensor_from_fpf(sensor.FPF_id, sensor_id)

        sensor_data = SensorSerializer(sensor).data

        return Response({**sensor_data, "connection": fpf_sensor_info}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Generate a new uuid for the sensor.
        Forward required sensor information to the FPF with the newly created sensor id.
        If successful, create the sensor in the database.
        Requesting user must be a member of the organization.
        :param request:
        :return:
        """
        fpf_id = request.data.get('fpfId')

        if not is_member(request.user, get_organization_by_fpf_id(fpf_id).id):
            return Response(status=status.HTTP_403_FORBIDDEN)

        sensor = request.data.copy()
        sensor.pop('fpfId', None)

        # Generate a new UUID
        new_uuid = uuid.uuid4()

        fpf_sensor_config = {
            "id": str(new_uuid),
            "intervalSeconds": sensor.get('intervalSeconds'),
            "connectionType": sensor.get('connection', {}).get('connectionType'),
            "additionalInformation": sensor.get('connection', {}).get('additionalInformation', {})
        }

        try:
            create_sensor_at_fpf(fpf_id, fpf_sensor_config)

            sensor["id"] = str(new_uuid)
            create_sensor(fpf_id, sensor)
        except Exception:
            raise Exception("Unable to create sensor at FPF.")

        return Response(status=status.HTTP_200_OK)

    def put(self, request, sensor_id):
        """
        Update the sensor by its id
        The requesting user must be part of the organization.
        If technical details like interval or connection type changed, sync with fpf
        If this is successful, update the local database and return OK.
        Requesting user must be a member of the organization.
        :param sensor_id:
        :param request:
        :return:
        """
        data = request.data
        fpf_id = get_sensor(sensor_id).FPF_id

        if not is_member(request.user, get_organization_by_fpf_id(fpf_id).id):
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Update sensor on FPF
        update_fpf_payload = {
            "intervalSeconds": data.get("intervalSeconds"),
            "connectionType": data.get("connection", {}).get("connectionType"),
            "additionalInformation": data.get("connection", {}).get("additionalInformation", {})
        }
        update_sensor_at_fpf(sensor_id, fpf_id, update_fpf_payload)

        # Update sensor locally
        update_sensor_payload = {key: value for key, value in data.items() if key != "connection"}
        update_sensor(sensor_id, update_sensor_payload)

        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fpf_sensor_types(request, fpf_id):
    """
    Verify that the fpf exists
    try to send a request to the fpf
    :return:
    """
    if not is_member(request.user, get_organization_by_fpf_id(fpf_id).id):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if is_valid_uuid(fpf_id):
        sensor_types = get_sensor_types_from_fpf(fpf_id)
        return Response(sensor_types, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
