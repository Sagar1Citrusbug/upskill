from django.db.models.manager import BaseManager
from .models import User, UserFactory
from typing import Type


class UserServices:
    @staticmethod
    def get_user_factory() -> Type[UserFactory]:
        return UserFactory

    @staticmethod
    def get_user_repo() -> BaseManager[User]:
        return User.objects

    def get_user_by_id(self, id: str) -> User:
        return User.objects.get(id=id)

    def get_user_by_email(self, email: str) -> User:
        return User.objects.get(email=email)
