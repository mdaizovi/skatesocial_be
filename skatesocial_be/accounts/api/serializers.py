from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            # add image when i add the field
        )


class UserBasicSerializer(serializers.ModelSerializer):
    email_verified = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ("id", "username", "name", "email", "email_verified")
