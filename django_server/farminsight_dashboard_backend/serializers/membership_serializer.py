from rest_framework import serializers
from farminsight_dashboard_backend.models import Membership, MembershipRole, Userprofile, Organization
from .userprofile_serializer import UserprofileSerializer


class MembershipSerializer(serializers.ModelSerializer):
    userprofileId = serializers.PrimaryKeyRelatedField(
        source='userprofile',  # Maps this field to the 'userprofile' foreign key in the model
        queryset=Userprofile.objects.all()
    )
    organizationId = serializers.PrimaryKeyRelatedField(
        source='organization',  # Maps this field to the 'organization' foreign key in the model
        queryset=Organization.objects.all()
    )

    class Meta:
        model = Membership
        read_only_fields = ('id', 'createdAt')
        fields = ('id', 'membershipRole', 'createdAt', 'userprofileId', 'organizationId')

    def validate_membershipRole(self, value):
        allowed = MembershipRole.list()
        if value not in allowed:
            raise serializers.ValidationError(f"membershipRole must be one of {allowed}.")
        return value

    def validate(self, data):
        # Check that Membership doesn't already exist!
        membership = Membership.objects.filter(userprofile=data['userprofile'], organization=data['organization']).first()
        if membership is not None:
            raise serializers.ValidationError("This user is already a member of the Organization.")
        return data


class MembershipSerializerIncUserprofile(serializers.ModelSerializer):
    userprofile = UserprofileSerializer(read_only=True, fields=('id', 'name', 'email'))

    class Meta:
        model = Membership
        fields = ['id', 'membershipRole', 'createdAt', 'userprofile']