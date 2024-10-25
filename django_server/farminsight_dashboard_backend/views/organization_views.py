from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Organization, Userprofile, Membership


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_organization(request):
    org = Organization.objects.create(name=request.data['name'], isPublic=request.data['isPublic'])
    org.save()
    userprofile = Userprofile.objects.filter(id=request.user.id).first()
    membership = Membership.objects.create(organization=org, user=userprofile, membershipRole='owner')
    return Response({"message": "successful operation"}, status=status.HTTP_201_CREATED)
