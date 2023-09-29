import debug_toolbar
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from dds.interface.user.urls import router as user_router


from dds.interface.role.urls import (
    router as role_router,
)
from dds.interface.company.urls import (
    router as company_router,
)


ENABLE_API = settings.ENABLE_API
PROJECT_URL = ""
API_SWAGGER_URL = "api/v0/"
REDIRECTION_URL = API_SWAGGER_URL if ENABLE_API else PROJECT_URL

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
    path(API_SWAGGER_URL, include(role_router.urls)),
    path(API_SWAGGER_URL, include(company_router.urls)),
    path("api/v0/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("__debug__/", include(debug_toolbar.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
