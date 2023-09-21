"""This is a model module to store UserRole data in to the database"""
import uuid
from django.db import models

from dataclasses import dataclass

from base_model import AuditModelMixin
from dds.utils import UserID

from dds.domain.company.models import CompanyID
from dds.domain.role.models import RoleID


@dataclass(frozen=True)
class UserRoleID:
    """
    This is a value object that should be used to generate and pass the UserID to the UserRoleFactory
    """

    value: uuid.UUID


# ----------------------------------------------------------------------
# UserRole Model
# ----------------------------------------------------------------------


class UserRole(AuditModelMixin):
    """
    Represents UserRole model
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    role_id = models.UUIDField(blank=False, null=False)
    user_id = models.UUIDField(blank=False, null=False)
    company_id = models.UUIDField(blank=False, null=False)

    class Meta:
        verbose_name = "UserRole"
        verbose_name_plural = "UserRoles"
        db_table = "userrole"


class UserRoleFactory:
    @staticmethod
    def build_entity(
        id: UserRoleID, role_id: RoleID, user_id: UserID, company_id: CompanyID
    ) -> UserRole:
        return UserRole(
            id=id.value,
            role_id=role_id.value,
            user_id=user_id.value,
            company_id=company_id.value,
        )

    @classmethod
    def build_entity_with_id(
        cls, role_id: RoleID, user_id: UserID, company_id: CompanyID
    ) -> UserRole:
        """This is a factory method used for build an instance of UserRole"""
        entity_id = UserRoleID(uuid.uuid4())
        return cls.build_entity(
            id=entity_id, role_id=role_id, user_id=user_id, company_id=company_id
        )
