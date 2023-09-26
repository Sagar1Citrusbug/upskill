from django.db.models.manager import BaseManager
from .models import UserRole, UserRoleFactory
from typing import Type


# class UserRoleServices:
#     @staticmethod
#     def get_user_role_factory() -> Type[UserRoleFactory]:
#         return UserRoleFactory

#     @staticmethod
#     def get_user_role_repo() -> BaseManager[UserRole]:
#         return UserRole.objects

#     def get_user_role_by_id(self, id: str) -> UserRole:
#         return UserRole.objects.get(id=id)
