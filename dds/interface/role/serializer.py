from rest_framework import serializers
from dds.domain.role.models import Role


class RoleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "is_active"]


class RoleCreateSerializer(RoleRetrieveSerializer):
    class Meta(RoleRetrieveSerializer.Meta):
        fields = ["name"]

    extra_kwargs = {"name": {"required": True}}
