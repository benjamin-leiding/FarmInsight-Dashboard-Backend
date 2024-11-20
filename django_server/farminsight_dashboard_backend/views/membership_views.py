from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from farminsight_dashboard_backend.serializers.update_membership_serializer import MembershipUpdateSerializer
from farminsight_dashboard_backend.services import (
    create_membership,
    update_membership,
    remove_membership
)
from farminsight_dashboard_backend.utils import is_valid_uuid


class MembershipView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a membership
        :param request:
        :return:
        """
        membership_serializer = create_membership(request.user, request.data)
        return Response(membership_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, membership_id):
        """
        Only admins can promote users to admins
        :param request:
        :param membership_id:
        :return:
        """
        membership_role = request.data.get('membershipRole')

        serializer = MembershipUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if is_valid_uuid(membership_id):
            update_membership(membership_id, request.user, membership_role)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, membership_id):
        """
        Only admins can delete users
        :param request:
        :param membership_id:
        :return:
        """
        if is_valid_uuid(membership_id):
            remove_membership(membership_id, request.user)

        return Response(status=status.HTTP_200_OK)

