from rest_framework import serializers
from farminsight_dashboard_backend.models import Userprofile


class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        read_only_fields = ('id', 'systemRole')
        fields = ('id', 'name', 'email', 'systemRole')
