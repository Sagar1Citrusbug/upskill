from django.db.models.query import QuerySet
from django.db import transaction
from dds.domain.company.models import Company
from dds.domain.company.services import CompanyServices
from dds.utils.custom_exceptions import (
    CompanyException,
    CompanyNotFoundException,
    CompanyAlreadyExistsException,
)


class CompanyAppServices:
    def __init__(self) -> None:
        self.company_services = CompanyServices()

    def list_companies(self) -> QuerySet[Company]:
        """This method will return list of Companies."""

        return self.company_services.get_company_repo().filter(is_active=True)

    def create_company(self, data: str) -> Company:
        company_name = data.get("name")
        company_exists = self.list_companies().filter(name=company_name.lower())
        if company_exists:
            raise CompanyAlreadyExistsException(
                "company-exist-exception", "This Company name is already exists."
            )
        try:
            with transaction.atomic():
                company_factory = self.company_services.get_company_factory()
                company_obj = company_factory.build_entity(name=company_name.lower())
                company_obj.save()
                return company_obj
        except Exception as e:
            raise CompanyException(item="company-exception", message=str(e))

    def get_company_by_user_id(self, user_id) -> QuerySet[Company]:
        try:
            user_role = self.user_role_app_services.list_user_roles().get(
                user_id=user_id
            )
            return self.company_services.get_company_repo().filter(
                id=user_role.company_id
            )
        except Exception as e:
            raise CompanyNotFoundException("company-exception", str(e))
