
import debug_toolbar
from django.contrib import admin
from django.urls import path

from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from .user import views
from django.conf import settings
from django.views.generic.base import RedirectView
from dds.interface.user.urls import router as user_router
# from dds.interface.objective.urls import router as objective_router
# from focus_power.interface.prioritized_tasks.urls import (
    # router as prioritized_tasks_router,
# )
# from dds.interface.role.urls import (
#     router as role_router,
# )
# from focus_power.interface.division.urls import (
#     router as division_router,
# )
# from focus_power.interface.reportee_tracker.urls import (
#     router as reportee_tracker_router,
# )
# from focus_power.interface.kpi.urls import router as kpi_router
# from focus_power.interface.calender_manager.urls import router as calender_router
# from focus_power.interface.initiative.urls import router as initiative_router
# from focus_power.interface.process.urls import router as process_router
# from focus_power.interface.recurring_activities.urls import (
    # router as recurring_activity_router,
# )


# from .user.views import GoogleAuthView


# import urls from interface layer modules

ENABLE_API = settings.ENABLE_API
PROJECT_URL = ""
API_SWAGGER_URL = "api/v0/"
REDIRECTION_URL = API_SWAGGER_URL if ENABLE_API else PROJECT_URL

# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("superadmin/", admin.site.urls),
    path("", RedirectView.as_view(url="api/v0/", permanent=False)),
]

urlpatterns += [
    path(
        API_SWAGGER_URL,
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(API_SWAGGER_URL, include(user_router.urls)),
    # path(API_SWAGGER_URL, include(objective_router.urls)),
    # path(API_SWAGGER_URL, include(prioritized_tasks_router.urls)),
    # path(API_SWAGGER_URL, include(reportee_tracker_router.urls)),
    # path(API_SWAGGER_URL, include(kpi_router.urls)),
    # path(API_SWAGGER_URL, include(calender_router.urls)),
    # path(API_SWAGGER_URL, include(role_router.urls)),
    # path(API_SWAGGER_URL, include(division_router.urls)),
    # path(API_SWAGGER_URL, include(initiative_router.urls)),
    # path(API_SWAGGER_URL, include(process_router.urls)),
    # path(API_SWAGGER_URL, include(recurring_activity_router.urls)),
    path("api/v0/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("__debug__/", include(debug_toolbar.urls)),
]

# media url

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
