from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dds.interface.role.pagination import RolesPagination
from dds.application.role.services import RolesAppServices
from .serializer import RoleRetrieveSerializer, RoleCreateSerializer
from dds.utils.custom_exceptions import (
    RoleException,
    RoleNameException,
    RoleNameAlreadyExistsException,
)
from dds.utils.custom_response import APIResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


class RoleViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    # authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAuthenticated,)
    pagination_class = RolesPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()

        return context

    def get_queryset(self):
        self.role_app_services = RolesAppServices()
        queryset = self.role_app_services.list_roles().order_by("-created_at")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RoleRetrieveSerializer
        if self.action == "create":
            return RoleCreateSerializer

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
            message = "Successfully listed all roles."
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
                role_app_services = RolesAppServices()
                role_obj = role_app_services.create_role_by_dict(
                    data=serializer.data,
                )
                response = RoleRetrieveSerializer(
                    instance=role_obj,
                    context={
                        "user": self.request.user,
                    },
                )
                return APIResponse(
                    data=response.data, message="Successfully created new role"
                )
            except (
                RoleNameAlreadyExistsException,
                RoleNameException,
            ) as e:
                return APIResponse(
                    status_code=e.status_code,
                    errors=e.error_data(),
                    message=e.message,
                    for_error=True,
                )
            except RoleException as e:
                return APIResponse(
                    status_code=e.status_code,
                    errors=e.error_data(),
                    message="An error occurred while creating role",
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
