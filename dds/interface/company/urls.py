from dds.interface.company.views import CompanyViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"company", CompanyViewSet, basename="company")
