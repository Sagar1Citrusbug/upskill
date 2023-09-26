from rest_framework import serializers
from dds.domain.company.models import Company
from dds.application.role.services import Role


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ["created_at"]


class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=60, required=True)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
