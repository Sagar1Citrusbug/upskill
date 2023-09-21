"""This is a model module to store Users data in to the database"""
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from ...utils import asdict
from dataclasses import dataclass, field
from dataclass_type_validator import dataclass_validate

import uuid

from base_model import AuditModelMixin

from typing import Union


@dataclass(frozen=True)
class UserID:
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """

    id: uuid.UUID = field(init=False, default_factory=uuid.uuid4)


@dataclass_validate(before_post_init=True)
@dataclass(frozen=False)
class UserPersonalData:
    """
    This is a value object that should be used to pass user personal data to the UserFactory
    """

    email: str
    username: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None

    def __post_init__(self):
        validate_email(self.email)


@dataclass_validate(before_post_init=True)
@dataclass(frozen=True)
class UserBasePermissions:
    """
    This is a value object that should be used to pass user base permissions to the UserFactory
    """

    is_staff: bool
    is_active: bool


class UserManagerAutoID(UserManager):
    """
    A User Manager that sets the uuid on a model when calling the create_superuser function.
    """

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if id not in extra_fields:
            extra_fields = dict(extra_fields, id=UserID().id, is_verified=True)

        return self._create_user(username, email, password, **extra_fields)


# ----------------------------------------------------------------------
# User Model
# ----------------------------------------------------------------------


class User(AbstractUser, AuditModelMixin):
    """
    A User replaces django's default user id with a UUID that should be created by the application, not the database.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True, blank=False, null=False)

    is_verified = models.BooleanField(default=False)

    profile_image = models.ImageField(upload_to="user_profile/", blank=True, null=True)
    objects = UserManagerAutoID()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"


class UserFactory:
    @staticmethod
    def build_entity_with_id(
        password: str,
        personal_data: UserPersonalData,
        base_permissions: UserBasePermissions,
    ):
        """This is a factory method used for build an instance of User"""

        personal_data_dict = asdict(personal_data, skip_empty=True)
        base_permissions_dict = asdict(base_permissions, skip_empty=True)
        password = make_password(password=password)
        return User(
            id=UserID().id,
            **personal_data_dict,
            **base_permissions_dict,
            password=password
        )
