from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions
from dj_rest_auth.serializers import LoginSerializer
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSerializer,
)

from rest_framework_simplejwt.tokens import RefreshToken

from ..authentication import DecadeRefreshToken

User = get_user_model()


class DualLogInSerializer(LoginSerializer):
    def _validate_username_email(self, username, email, password):
        """Subclassed to allow login with username or email (systemwide),
        but not confuse user by telling them they can supply username
        """
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _("All fields must be provided")
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")
        user = None

        # Authentication through either username or email.
        # Specifying in settings is irrelevant.
        user = self._validate_username_email(username, email, password)
        if user:
            if not user.is_active:
                fail_msg_list = [_("Account is inactive")]
                raise exceptions.ValidationError(fail_msg_list)
        else:
            fail_msg_list = [_("Log in failed")]
            raise exceptions.ValidationError(fail_msg_list)

        attrs["user"] = user
        return attrs


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "name",
            "email",
        )


class TokenSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    def get_access(self, obj):
        self.token = DecadeRefreshToken.for_user(obj)
        return str(self.token.access_token)

    def get_refresh(self, obj):
        self.token = DecadeRefreshToken.for_user(obj)
        return str(self.token)

    class Meta:
        model = User
        fields = (
            "access",
            "refresh",
        )


class UserTokenSerializer(serializers.Serializer):
    user = UserBasicSerializer()
    tokens = TokenSerializer()
