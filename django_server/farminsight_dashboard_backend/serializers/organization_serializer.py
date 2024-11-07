from rest_framework import serializers
from farminsight_dashboard_backend.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        read_only_fields = ('id',)
        fields = ('id', 'name', 'isPublic')
