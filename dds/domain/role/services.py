from django.db.models.manager import BaseManager
from .models import Role, RoleFactory
from typing import Type


class RoleServices:
    @staticmethod
    def get_role_factory() -> Type[RoleFactory]:
        return RoleFactory

    @staticmethod
    def get_role_repo() -> BaseManager[Role]:
        return Role.objects

    def get_role_by_id(self, id: str) -> Role:
        return Role.objects.get(id=id)
