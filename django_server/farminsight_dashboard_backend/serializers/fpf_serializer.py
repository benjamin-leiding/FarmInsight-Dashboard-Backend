from rest_framework import serializers
from farminsight_dashboard_backend.models import FPF


class FPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = FPF
        read_only_fields = ('id',)
        fields = ('id', 'name', 'isPublic', 'sensorServiceIp', 'cameraServiceIp', 'address', 'organization')

    def validate(self, data):
        fpfs = FPF.objects.filter(name=data['name'], organization=data['organization'])
        if len(fpfs) > 0:
            raise serializers.ValidationError({"name":"This name is already taken for this organization"})
        return data
