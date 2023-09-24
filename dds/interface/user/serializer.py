from rest_framework import serializers
from dds.domain.user.models import User
from dds.domain.company.models import Company
from dds.application.company.services import CompanyAppServices
from dds.application.role.services import Role
from dds.application.role.services import UserRolesAppServices


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


class UserListSerializer(serializers.ModelSerializer):
   
    # company_services = CompanyAppServices()
    # role_services = UserRolesAppServices()
    # company  =  serializers.SerializerMethodField()
    # role =  serializers.SerializerMethodField()

    # def get_company(self , obj):
        
    #     company_obj =  self.company_services.get_company_by_user_id(obj.id)
    #     return company_obj.name    
    
    # def get_role(self, obj):
         
    #     role_obj = self.role_services.get_user_role_by_user_id(obj.id)
    #     return role_obj.name

    class Meta:
        model = User
        fields = ["id", "email", "is_verified"]
