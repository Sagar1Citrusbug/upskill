"""This is a model module to store Roles data in to the database"""
from django.db import models

from dataclasses import dataclass

import uuid
from dds.utils.base_model import AuditModelMixin


@dataclass(frozen=True)
class RoleID:
    """
    This is a value object that should be used to generate and pass the RoleID to the RoleFactory
    """

    value: uuid.UUID


# ----------------------------------------------------------------------
# Role Model
# ----------------------------------------------------------------------


class Role(AuditModelMixin):
    """
    Represents Role model
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        db_table = "role"


class RoleFactory:
    @classmethod
    def build_entity_with_id(
        cls,
        name: str,
    ) -> Role:
        """This is a factory method used for build an instance of Role"""
        entity_id = RoleID(uuid.uuid4())
        return cls.build_entity(id=entity_id, name=name)

    @staticmethod
    def build_entity(
        id: RoleID,
        name: str,
    ) -> Role:
        return Role(id=id.value, name=name)
