from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendRequest(models.Model):

    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    initiated_at = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="user initiated wants to connect with"
    )

    def __str__(self):
        return "<{}> {} to {}".format(
            self.__class__.__name__, self.initiated_by, self.target
        )


class Friendship(models.Model):

    users = models.ManyToManyField(User)

    def clean(self):
        if self.users.count() != 2:
            raise ValidationError("Must have exactly 2 people in this friendship")

    def __str__(self):
        user_str = ", ".join([x for x in self.users.all()])
        return "<{}>: {}".format(self.__class__.__name__, user_str)


class Crew(models.Model):
    """Basically a Facebook Group, for post privacy"""

    name = models.CharField(max_length=100)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)

    def __str__(self):
        return "<{}>: {} by {}".format(
            self.__class__.__name__, self.name, self.owned_by
        )
