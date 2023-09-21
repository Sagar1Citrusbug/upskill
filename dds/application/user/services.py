from django.db.models.query import QuerySet
from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password
from dds.domain.user.models import (
    User,
    UserPersonalData,
    UserBasePermissions,
)
from dds.domain.user.services import UserServices
from dds.utils.utils import generate_password
from dds.application.company.services import (
    CompanyAppServices,
)
from dds.application.role.services import UserRolesAppServices

from dds.utils.custom_exceptions import (
    UserAlreadyExistsException,
    UserDeletionException,
    MailNotSendException,
)


class UserAppServices:
    def __init__(
        self,
    ) -> None:
        self.user_services = UserServices()

        self.company_app_services = CompanyAppServices(log=self.log)
        self.user_roles_app_service = UserRolesAppServices(log=self.log)

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
                    "User already Exists",
                    f"{user_exists[0].email} already exists.",
                    self.log,
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
                if settings.ENABLE_MAILS:
                    template_data = dict(
                        subject="Welcome to Focus Power - Verify your email address",
                        verification_url=self.token_url_generator(
                            user=user_obj, use_case="new_user"
                        ),
                        first_name=user_obj.first_name,
                    )
                    self.mail_services.send_mail(
                        email=user_obj.email,
                        subject=template_data.get("subject"),
                        template_data=template_data,
                        template_id=settings.NEW_USER_VERIFICATION_EMAIL_TEMPLATE,
                    )

                return user_obj
            except Exception as e:
                if isinstance(e, MailNotSendException):
                    raise e

    def get_user_by_pk(self, pk) -> User:
        try:
            return self.list_users().get(pk=pk)
        except Exception as e:
            raise Exception()

    def delete_user_by_pk(self, pk) -> User:
        instance = self.get_user_by_pk(pk=pk)
        instance.delete()
        return instance

    def add_user_from_dict(self, data: dict, user: User, company_id: str) -> User:
        with transaction.atomic():
            email = data.get("email", None)
            reporting_to_id = data.get("reporting_to", None)
            first_name = data.get("first_name", None)
            last_name = data.get("last_name", None)

            user_exists = self.user_services.get_user_repo().filter(email=email)
            if user_exists:
                raise UserAlreadyExistsException(
                    "User already exists",
                    f"{user_exists[0].email} already exists.",
                    self.log,
                )
            senior_obj = self.list_users().filter(id=reporting_to_id)
            if not senior_obj:
                raise Exception()
            user_personal_data = UserPersonalData(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
            )
            user_base_permissions = UserBasePermissions(is_staff=False, is_active=False)
            user_factory_method = self.user_services.get_user_factory()
            password = generate_password()
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

    def update_user_from_dict(self, data: dict, email: str) -> User:
        with transaction.atomic():
            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            password = data.get("password")
            user_obj = self.user_services.get_user_repo().filter(email=email).first()
            if not user_obj:
                raise Exception()
            if user_obj.is_active == True and user_obj.is_verified == True:
                raise Exception()
            try:
                with transaction.atomic():
                    user_obj.first_name = first_name
                    user_obj.last_name = last_name
                    user_obj.password = make_password(password=password)
                    user_obj.is_active = True
                    user_obj.is_verified = True
                    user_obj.save()
                    return user_obj
            except Exception as e:
                raise Exception()

    def update_status(self, data: dict, user: User, user_id: str) -> dict:
        self.__check_user_division_ceo(user=user)
        is_active = data.get("is_active", None)
        is_allow_radical_settings = data.get("is_allow_radical_settings", None)
        user_obj = self.get_user_by_pk(pk=user_id)
        if not user_obj:
            raise Exception()
        try:
            with transaction.atomic():
                if is_active is not None:
                    user_obj.is_active = is_active
                    user_obj.save()
                if is_allow_radical_settings is not None:
                    user_obj.is_allow_radical_settings = is_allow_radical_settings
                    user_obj.save()
                return {
                    key: getattr(user_obj, key)
                    for key in data.keys()
                    if hasattr(user_obj, key)
                }
        except Exception as e:
            raise Exception()

    def destroy_user_by_pk(self, user: User, user_id: str):
        with transaction.atomic():
            if str(user.id) == user_id:
                raise UserDeletionException(
                    "user-deletion-exception", "This user cannot be deleted", self.log
                )
            self.__check_user_division_ceo(user=user)

            user_instance = self.get_user_by_pk(pk=user_id)
            if not self.user_roles_app_service.is_users_from_same_company(
                users=[user, user_instance]
            ):
                raise Exception("company-exception", "User is not from same company")
            user_instance_company = self.company_app_services.get_company_by_user_id(
                user_id=user_instance.id
            )
            user_role_instance = self.user_roles_app_service.list_user_roles().filter(
                user_id=user_instance.id, company_id=user_instance_company[0].id
            )
            user_role_instance.delete()

            user_instance.delete()

            return True
