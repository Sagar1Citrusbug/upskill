from django.db.models.query import QuerySet
from dds.domain.company.models import Company
from dds.domain.company.services import CompanyServices
from dds.application.role.services import UserRolesAppServices
from dds.utils.custom_exceptions import (
    CompanyNotFoundException,
)


class CompanyAppServices:
    def __init__(self) -> None:
        self.company_services = CompanyServices()
        self.user_role_app_services = UserRolesAppServices()

    def list_companies(self) -> QuerySet[Company]:
        """This method will return list of Companies."""
        return self.company_services.get_company_repo().filter(is_active=True)

    def create_company(self, company_name: str) -> Company:
        company_factory_method = self.company_services.get_company_factory()
        company_obj = company_factory_method.build_entity_with_id(name=company_name)
        company_obj.save()
        return company_obj

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
