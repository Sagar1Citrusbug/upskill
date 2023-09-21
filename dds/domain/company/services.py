from django.db.models.manager import BaseManager
from .models import Company, CompanyFactory
from typing import Type


class CompanyServices:
    @staticmethod
    def get_company_factory() -> Type[CompanyFactory]:
        return CompanyFactory

    @staticmethod
    def get_company_repo() -> BaseManager[Company]:
        return Company.objects

    def get_company_by_id(self, id: str) -> Company:
        return Company.objects.get(id=id)
