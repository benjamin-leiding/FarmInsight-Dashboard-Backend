from rest_framework.permissions import IsAuthenticated
from farminsight_dashboard_backend.services import create_fpf, get_fpf_by_id
from rest_framework import views, status
from rest_framework.response import Response


class FpfView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fpf_id):
        return Response(get_fpf_by_id(fpf_id), status=status.HTTP_200_OK)

    def post(self, request):
        fpf = create_fpf(request.data)
        return Response(fpf.data, status=status.HTTP_201_CREATED)
