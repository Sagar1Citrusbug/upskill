from rest_framework import serializers
from dds.domain.user.models import User
from dds.domain.company.models import Company
from dds.application.company.services import CompanyAppServices
from dds.application.role.services import Role


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ["created_at"]


class UserSerializer(serializers.ModelSerializer):
    company_details = serializers.SerializerMethodField()

    def get_company_details(self, obj):
        company_app_services = CompanyAppServices()
        return CompanySerializer(
            company_app_services.get_company_by_user_id(user_id=obj.id).first()
        ).data

    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class OrganizationAddUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150, required=True)
    role = serializers.UUIDField(required=True)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)


class UserListSerializer(UserSerializer):
    company_details = None

    class Meta:
        model = User
        exclude = [
            "password",
            "groups",
            "user_permissions",
            "is_superuser",
            "username",
            "is_staff",
            "date_joined",
            "created_at",
        ]
