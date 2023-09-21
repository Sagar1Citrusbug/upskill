import re
from typing import List
from django.db.models.query import QuerySet
from django.db import transaction
from django.conf import settings

from dds.domain.role.models import Role, RoleID
from dds.domain.role.user_role.models import UserRole
from dds.domain.company.models import CompanyID
from dds.domain.role.services import RoleServices
from dds.domain.user.models import User
from dds.domain.role.user_role.services import UserRoleServices
from utils.custom_exceptions import (
    UserRoleException,
    RoleException,
    RoleNameException,
    RoleNameAlreadyExistsException,
)


from utils import UserID


class RolesAppServices:
    def __init__(self) -> None:
        self.role_services = RoleServices()

    def create_role_by_dict(self, user: User, data: dict) -> Role:
        name = data.get("name")
        if not re.match("^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]$", name):
            raise RoleNameException(
                "role-name-exception", "Role name should be alphanumeric.", self.log
            )

        exists_role = self.list_roles(user=user).filter(name=name.lower())
        if exists_role:
            raise RoleNameAlreadyExistsException(
                "role-exist-exception", "This role name is already exists.", self.log
            )
        try:
            with transaction.atomic():
                role_factory = self.role_services.get_role_factory()
                role_obj = role_factory.build_entity_with_id(name=name.lower())
                role_obj.save()
                return role_obj
        except Exception as e:
            raise RoleException(item="role-exception", message=str(e), log=self.log)


class UserRolesAppServices:
    def __init__(self) -> None:
        self.role_app_services = RolesAppServices(log=self.log)
        self.user_role_services = UserRoleServices()

    def list_user_roles(self) -> QuerySet[UserRole]:
        """This method will return list of UserRoles."""
        return self.user_role_services.get_user_role_repo().filter(is_active=True)

    def create_ceo_user_role(self, user: User, company_id: CompanyID) -> UserRole:
        try:
            with transaction.atomic():
                role_queryset = (
                    self.role_app_services.role_services.get_role_repo().filter(
                        name__icontains="ceo"
                    )
                )
                if role_queryset:
                    role_id = RoleID(value=role_queryset[0].id)
                    user_id = UserID(value=user.id)
                    user_role_factory = self.user_role_services.get_user_role_factory()
                    user_role_obj = user_role_factory.build_entity_with_id(
                        role_id=role_id, user_id=user_id, company_id=company_id
                    )
                    user_role_obj.save()
                    return user_role_obj
        except Exception as e:
            raise UserRoleException("user-role-exception", str(e))

    def create_user_role(self, user_id, company_id, role_id) -> UserRole:
        try:
            with transaction.atomic():
                role_id = RoleID(value=role_id)
                user_id = UserID(value=user_id)
                company_id = CompanyID(value=company_id)
                user_role_factory = self.user_role_services.get_user_role_factory()
                user_role_obj = user_role_factory.build_entity_with_id(
                    role_id=role_id, user_id=user_id, company_id=company_id
                )
                user_role_obj.save()
                return user_role_obj
        except Exception as e:
            raise UserRoleException("user-role-exception", str(e))

    def get_user_role_by_user_id(self, user_id) -> UserRole:
        return self.list_user_roles().get(user_id=user_id)

    def is_users_from_same_company(self, users: List[User]) -> bool:
        """Returns True if all users belong to the same company, False otherwise."""
        company_ids = set()
        for user in users:
            responsible_person_user_role = self.list_user_roles().filter(
                user_id=user.id
            )
            if responsible_person_user_role:
                company_ids.add(responsible_person_user_role[0].company_id)
        return len(company_ids) == 1
