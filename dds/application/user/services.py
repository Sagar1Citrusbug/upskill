from django.db.models.query import QuerySet
from django.db import transaction
from dds.domain.user.models import (
    User,
    UserPersonalData,
    UserBasePermissions,
)
from dds.domain.user.services import UserServices
from dds.application.company.services import (
    CompanyAppServices,
)

from dds.utils.custom_exceptions import (
    UserAlreadyExistsException,
)


class UserAppServices:
    def __init__(
        self,
    ) -> None:
        self.user_services = UserServices()
        self.company_app_services = CompanyAppServices()

    def list_users(self) -> QuerySet[User]:
        """This method will return list of users."""

        return self.user_services.get_user_repo().all()

    def create_user_from_dict(self, data: dict) -> User:
        """This method will create user from dict."""
        with transaction.atomic():
            email = data.get("email", None)
            first_name = data.get("first_name", None)
            last_name = data.get("last_name", None)
            password = data.get("password", None)
            user_exists = self.user_services.get_user_repo().filter(email=email)
            if user_exists:
                raise UserAlreadyExistsException(
                    "User already Exists", f"{user_exists[0].email} already exists."
                )
            user_personal_data = UserPersonalData(
                email=email, first_name=first_name, last_name=last_name, username=email
            )
            user_base_permissions = UserBasePermissions(is_staff=False, is_active=True)
            user_factory_method = self.user_services.get_user_factory()
            try:
                user_obj = user_factory_method.build_entity_with_id(
                    password=password,
                    personal_data=user_personal_data,
                    base_permissions=user_base_permissions,
                )
                user_obj.save()

                return user_obj
            except Exception as e:
                raise e
