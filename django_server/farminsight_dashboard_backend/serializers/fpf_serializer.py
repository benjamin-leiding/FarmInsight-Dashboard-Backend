from rest_framework import serializers
from ..models import FPF


class FPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = FPF
        fields = '__all__'