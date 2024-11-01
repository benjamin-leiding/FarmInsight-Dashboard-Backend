from rest_framework import serializers
from farminsight_dashboard_backend.models import FPF


class FPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = FPF
        fields = '__all__'