from dds.interface.role.views import RoleViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"roles", RoleViewSet, basename="roles")
