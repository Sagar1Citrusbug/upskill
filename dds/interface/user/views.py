from django.contrib.auth import authenticate
from django.utils.decorators import decorator_from_middleware_with_args

# from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework import status

# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# local imports
from .serializer import (
    UserSerializer,
    OrganizationAddUserSerializer,
    UserListSerializer,
)
# from .. import open_api
from .pagination import OrganizationUserPagination

# from .filters import OrganizationUserFilter

# app imports
from dds.application.user.services import UserAppServices

from dds.utils.custom_exceptions import (
    UserAlreadyExistsException,
    MailNotSendException,
    UserDeletionException,
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

    # access_control = decorator_from_middleware_with_args(MiddlewareWithLogger)

    def get_queryset(self):
        user_app_services = UserAppServices()
        return user_app_services.list_users().order_by("?")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update()
        return context

    def get_serializer_class(self):
        return UserSerializer


    
    @action(detail=False, methods=["post"], name="create_user")
 
    def sign_up(self, request):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        if serializer_data.is_valid():
            try:
                user_data = UserAppServices(log=self.log).create_user_from_dict(
                    data=serializer_data.data
                )
                serialized_user_data = UserSerializer(
                    instance=user_data,
                    context={
                        "log": self.log,
                    },
                )
                return response(
                    status=status.HTTP_201_CREATED,
                    data=serialized_user_data.data,
                   
                )
            except Exception as use:
                return response(
                    {"message": "User has not been created from provided data"}
                )
           