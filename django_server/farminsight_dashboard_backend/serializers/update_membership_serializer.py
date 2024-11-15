from rest_framework import serializers


class MembershipUpdateSerializer(serializers.Serializer):
    membershipRole = serializers.CharField(max_length=256)

    def validate_membershipRole(self, value):
        if value != "admin":
            raise serializers.ValidationError(f"Invalid role. Expected admin role.")
        return value
