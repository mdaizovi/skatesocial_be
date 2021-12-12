from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from dj_rest_auth.views import LoginView as RestAuthLoginView
from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import (
    DualLogInSerializer,
    LoginResponseSerializer,
    UserBasicSerializer,
    EmailTokenObtainPairSerializer,
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

    def get_response_serializer(self):
        return LoginResponseSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if self.token:
            user_serializer = UserBasicSerializer(instance=self.user)

            token_data = {
                "refresh": str(self.token),
                "access": str(self.token.access_token),
            }
            print("token_data")
            print(token_data)
            token_serializer = EmailTokenObtainPairSerializer(data=token_data)

            data = {
                "user": user_serializer.data,
                "token": token_serializer.initial_data,
            }
            print(data)
            serializer = serializer_class(
                data=data,
                context=self.get_serializer_context(),
            )
            print("end")
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        response = Response(serializer.initial_data, status=status.HTTP_200_OK)
        return response
