from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from .views import LoginView

urlpatterns = [
    # api/auth/login/ Should be before rest auth LoginView to override it
    re_path("login/", LoginView.as_view(), name="app-login"),
    # subclass must be before rest_auth.url bc first matching url is what's used.
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include("dj_rest_auth.urls")),
]
