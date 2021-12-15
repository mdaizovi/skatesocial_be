from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from allauth.account import app_settings as allauth_settings
from dj_rest_auth.views import LoginView as RestAuthLoginView
from dj_rest_auth.registration.views import RegisterView as RestAuthRegisterView
from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import (
    DualLogInSerializer,
    UserBasicSerializer,
    TokenSerializer,
    UserTokenSerializer,
)
from ..authentication import DecadeRefreshToken

User = get_user_model()

# @authentication_classes([]) is important because otherwise the client might send a bad token
# and there will be an 'error decoding signature' that can cause the entire login to fail
# with no notification


@authentication_classes([])
class LoginView(RestAuthLoginView):
    """Subclassed LoginView from django-rest-auth"""

    serializer_class = DualLogInSerializer

    def login(self):
        self.user = self.serializer.validated_data["user"]
        token = DecadeRefreshToken.for_user(self.user)
        self.token = token

    def get_response(self):

        if self.token:
            user_serializer = UserBasicSerializer(instance=self.user)
            token_serializer = TokenSerializer(instance=self.user)
            data = {"user": user_serializer.data, "tokens": token_serializer.data}
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserTokenSerializer(
            data=data, context=self.get_serializer_context()
        )
        serializer.is_valid()
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response


# to get rid of csrf, not needed for login or register.
@authentication_classes([])
class RegisterView(RestAuthRegisterView):
    def get_response_data(self, user):
        if (
            allauth_settings.EMAIL_VERIFICATION
            == allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            return {"detail": _("Verification e-mail sent.")}

        user_serializer = UserBasicSerializer(instance=user)
        token_serializer = TokenSerializer(instance=user)
        data = {"user": user_serializer.data, "tokens": token_serializer.data}
        serializer = UserTokenSerializer(
            data=data, context=self.get_serializer_context()
        )
        serializer.is_valid()
        return serializer.data
