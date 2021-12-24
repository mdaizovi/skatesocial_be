from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions
from ..models import FriendRequest, Friendship, Crew

User = get_user_model()


class KeyModelSerializer(serializers.ModelSerializer):
    @classmethod
    def get_model_name(self, many=False):
        if many:
            model_name = str(self.Meta.model._meta.verbose_name_plural)
        else:
            model_name = self.Meta.model.__name__.lower()
        return model_name
        # return self.serializer_class.Meta.model._meta.verbose_name_plural


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("id",)


class FriendRequestRespondSerializer(serializers.Serializer):
    user_response = serializers.IntegerField(required=True)


class CrewUpdateSerializer(KeyModelSerializer):
    name = serializers.CharField(source="name", required=False)
    members = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), required=False
    )

    class Meta:
        model = Crew
        fields = ("id", "name", "members")
        depth = 1


class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            # add image when i add the field
        )


class CrewDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source="name",
        read_only=True,
    )
    # members = CrewMemberSerializer(source = "members", many=True)
    members = CrewMemberSerializer()

    class Meta:
        model = Crew
        fields = ("id", "name", "members")
