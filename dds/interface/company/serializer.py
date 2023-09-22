# django imports
from rest_framework import serializers
from dds.domain.company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name"]


extra_kwargs = {"name": {"required": True}}


class CompanyRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "is_active"]
