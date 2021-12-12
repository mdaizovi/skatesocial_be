from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # this is for browsable api login/logout
    path("api-auth/", include("rest_framework.urls")),
    # not redundant, notice difference between api-auth and api/auth
    path("api/auth/", include("auth.api.urls")),
]
