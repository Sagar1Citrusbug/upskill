from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework import status


from .serializer import (
    # UserListSerializer,
    UserCreateSerializer,
)
from dds.utils.custom_response import APIResponse
from .pagination import OrganizationUserPagination


# app imports
from dds.application.user.services import UserAppServices

from dds.utils.custom_exceptions import (
    AddUserException,
    UserAlreadyExistsException,
)


class BadRequest(APIException):
    status_code = 400
    default_detail = (
        "The request cannot be fulfilled, please try again with different parameters."
    )
    default_code = "bad_request"


class UserViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    paginator_class = OrganizationUserPagination

    def get_queryset(self):
        user_app_services = UserAppServices()
        return user_app_services.list_users().order_by("?")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update()
        return context

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer

        # return UserListSerializer

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        if serializer_data.is_valid():
            try:
                user_data = UserAppServices().create_user_from_dict(
                    data=serializer_data.data
                )

                return APIResponse(
                    status_code=status.HTTP_201_CREATED,
                    data=serializer_data.data,
                    message=f"user created Successfully.",
                )
            except AddUserException as use:
                return APIResponse(
                    status_code=use.status_code,
                    errors=use.error_data(),
                    message=f"An error occurred while Sign-up.",
                    for_error=True,
                )
            except UserAlreadyExistsException as uae:
                return APIResponse(
                    status_code=uae.status_code,
                    errors=uae.error_data(),
                    message=f"User already exists",
                    for_error=True,
                )
            except Exception as e:
                print(e, "---------error-----------")
                return APIResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    errors=e.args,
                    for_error=True,
                    general_error=True,
                )
        print("-----------hererer=============")
        return APIResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer_data.errors,
            message=f"Incorrect email or password",
            for_error=True,
        )

    # def list(self, request):
    #     serializer = self.get_serializer_class()
    #     try:
    #         queryset = self.get_queryset()
    #         paginator = self.paginator_class()
    #         paginated_queryset = paginator.paginate_queryset(queryset, request)
    #         serializer_data = serializer(
    #             paginated_queryset,
    #             many=True,
    #         )
    #         paginated_data = paginator.get_paginated_response(serializer_data.data).data
    #         message = "Successfully listed all Users."
    #         return APIResponse(data=paginated_data, message=message)

    #     except Exception as e:
    #         print(e, "------- error ---------")
    #         return APIResponse(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             errors=e.args,
    #             for_error=True,
    #             general_error=True,
    #         )
