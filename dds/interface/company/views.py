from rest_framework import viewsets
from rest_framework import status
from dds.interface.company.pagination import CompanyPagination
from dds.application.company.services import CompanyAppServices
from .serializer import CompanyRetrieveSerializer, CompanySerializer
from dds.utils.custom_exceptions import (
    CompanyAlreadyExistsException,
)
from dds.utils.custom_response import APIResponse


class CompanyViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    pagination_class = CompanyPagination

    def get_queryset(self):
        self.company_app_services = CompanyAppServices()
        queryset = self.company_app_services.list_companies().order_by("-created_at")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyRetrieveSerializer
        if self.action == "create":
            return CompanySerializer

    def list(self, request):
        serializer = self.get_serializer_class()
        try:
            queryset = self.get_queryset()
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer_data = serializer(
                paginated_queryset,
                many=True,
                context={
                    "request": self.request,
                    "user": self.request.user,
                },
            )
            paginated_data = paginator.get_paginated_response(serializer_data.data).data
            message = "Successfully listed all Companies."
            return APIResponse(data=paginated_data, message=message)

        except Exception as e:
            return APIResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=e.args,
                for_error=True,
                general_error=True,
            )

    def create(self, request):
        get_serializer = self.get_serializer_class()
        serializer = get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                company_app_services = CompanyAppServices()
                company_obj = company_app_services.create_company(serializer.data)
                response = CompanyRetrieveSerializer(
                    instance=company_obj,
                )
                return APIResponse(
                    data=response.data, message="Successfully created new Company"
                )
            except (CompanyAlreadyExistsException,) as e:
                return APIResponse(
                    status_code=e.status_code,
                    errors=e.error_data(),
                    message=e.message,
                    for_error=True,
                )

            except Exception as e:
                return APIResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    errors=e.args,
                    for_error=True,
                    general_error=True,
                )
        return APIResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors,
            message="Invalid data",
            for_error=True,
        )
