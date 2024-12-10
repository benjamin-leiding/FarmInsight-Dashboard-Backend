from farminsight_dashboard_backend.serializers import FPFFullSerializer
from farminsight_dashboard_backend.services import create_fpf, get_fpf_by_id, update_fpf_api_key, \
    get_visible_fpf_preview
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


class FpfView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fpf_id):
        return Response(FPFFullSerializer(get_fpf_by_id(fpf_id)).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = create_fpf(request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_fpf_api_key(request, fpf_id):
    """
    Generate a new apiKey and try to send it to the FPF.
    On success, save the new key in the database.
    :param request: 
    :param fpf_id: 
    :return: 
    """
    update_fpf_api_key(fpf_id)
    
    return Response(status=status.HTTP_200_OK)
    

@api_view(['GET'])
def get_visible_fpf(request):
    """
    Returns List of all FPFs visible to the user includes non public ones that user is member of
    :param request:
    :return:
    """
    user = None
    if request.user.is_authenticated:
        user = request.user
    serializer = get_visible_fpf_preview(user)
    return Response(serializer.data, status=status.HTTP_200_OK)