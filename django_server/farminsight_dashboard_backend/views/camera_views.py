from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from farminsight_dashboard_backend.serializers.camera_serializer import CameraSerializer
from farminsight_dashboard_backend.services import get_camera_by_id, update_camera, delete_camera, \
    get_fpf_by_id, create_camera


class CameraView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, camera_id):
        """
        Get a camera by its id
        :param request:
        :param camera_id:
        :return:
        """
        return Response(CameraSerializer(get_camera_by_id(camera_id)).data, status=status.HTTP_200_OK)

    def put(self, request, camera_id):
        """
        If incoming camera data is valid, update the camera by given id with the incoming data
        If the interval was updated, reschedule the job of the camera
        :param request:
        :param camera_id: id of the camera to update
        :return:
        """
        from farminsight_dashboard_backend.services import CameraScheduler
        serializer = CameraSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_interval = get_camera_by_id(camera_id).intervalSeconds

        camera = update_camera(camera_id, serializer.data)

        if camera.intervalSeconds != old_interval:
            CameraScheduler.get_instance().add_camera_job(camera.id)

        return Response(CameraSerializer(camera).data, status=status.HTTP_200_OK)

    def delete(self, request, camera_id):
        """
        Delete a camera by given id and the associated job
        :param request:
        :param camera_id:
        :return:
        """
        from farminsight_dashboard_backend.services import CameraScheduler
        CameraScheduler.get_instance().remove_camera_job(camera_id)
        delete_camera(camera_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_camera(request):
    """
    Create a new camera and schedule a new job
    :param request:
    :return:
    """
    from farminsight_dashboard_backend.services import CameraScheduler
    camera_data = request.data.get('camera')
    fpf_id = request.data.get('fpfId')

    get_fpf_by_id(fpf_id)
    CameraSerializer(data=camera_data).is_valid(raise_exception=True)
    camera = CameraSerializer(create_camera(fpf_id, camera_data)).data
    CameraScheduler.get_instance().add_camera_job(camera.get('id'))

    return Response(camera, status=status.HTTP_201_CREATED)
