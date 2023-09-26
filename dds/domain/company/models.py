"""This is a model module to store Companies data in to the database"""
from django.db import models


from dataclasses import dataclass

import uuid
from dds.utils.base_model import AuditModelMixin


@dataclass(frozen=True)
class CompanyID:
    """
    This is a value object that should be used to generate and pass the RoleID to the CompanyFactory
    """

    value: uuid.UUID


# ----------------------------------------------------------------------
# Company Model
# ----------------------------------------------------------------------


class Company(AuditModelMixin):
    """
    Represents Company model
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "company"


class CompanyFactory:
    @classmethod
    def build_entity_with_id(
        cls,
        name: str,
    ) -> Company:
        """This is a factory method used for build an instance of Company"""
        entity_id = CompanyID(uuid.uuid4())
        return cls.build_entity(id=entity_id, name=name)

    @staticmethod
    def build_entity(
        name: str,
    ) -> Company:
        return Company(name=name)
