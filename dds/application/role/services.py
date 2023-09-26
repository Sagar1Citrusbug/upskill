import re
from django.db.models.query import QuerySet
from django.db import transaction

from dds.domain.role.models import Role
from dds.domain.role.services import RoleServices

from dds.utils.custom_exceptions import (
    RoleException,
    RoleNameException,
    RoleNameAlreadyExistsException,
)


class RolesAppServices:
    def __init__(self) -> None:
        self.role_services = RoleServices()

    def list_roles(
        self,
    ) -> QuerySet[Role]:
        """This method will return list of Roles."""

        return (
            self.role_services.get_role_repo()
            .filter(is_active=True)
            .exclude(name__icontains="ceo")
        )

    def create_role_by_dict(self, data: dict) -> Role:
        name = data.get("name")
        if not re.match("^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]$", name):
            raise RoleNameException(
                "role-name-exception", "Role name should be alphanumeric."
            )

        exists_role = self.list_roles().filter(name=name.lower())

        if exists_role:
            raise RoleNameAlreadyExistsException(
                "role-exist-exception", "This role name is already exists."
            )
        try:
            with transaction.atomic():
                role_factory = self.role_services.get_role_factory()
                role_obj = role_factory.build_entity_with_id(name=name.lower())
                role_obj.save()
                return role_obj
        except Exception as e:
            raise RoleException(item="role-exception", message=str(e))
