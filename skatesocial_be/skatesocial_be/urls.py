from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

"""
POST is always for creating a resource ( does not matter if it was duplicated )
PUT is for checking if resource is exists then update , else create new resource
PATCH is always for update a resource
"""
urlpatterns = [
    path("admin/", admin.site.urls),
    # this is for browsable api login/logout
    path("rest-auth/", include("rest_framework.urls")),
    # not redundant, notice difference between api-auth and api/auth
    path("api/v1/auth/", include("auth.api.urls")),
    path("api/v1/search/", include("search.api.urls")),
    path("api/v1/network/", include("crew_network.api.urls")),
    path("api/v1/news/", include("news_feed.api.urls")),
]
