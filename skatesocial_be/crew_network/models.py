from .signals import remove_deleted_friend_from_crews
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save, pre_delete

User = get_user_model()


class FriendRequest(models.Model):

    initiated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="initiated_friend_requests"
    )
    initiated_at = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="user initiated wants to connect with",
        related_name="pending_friend_requests",
    )

    def __str__(self):
        return "<{}> {} to {}".format(
            self.__class__.__name__, self.initiated_by, self.target
        )


class Friendship(models.Model):

    users = models.ManyToManyField(User)

    def clean(self):
        if self.pk:  # don't run for first save
            if self.users.count() != 2:
                raise ValidationError("Must have exactly 2 people in this friendship")

    def __str__(self):
        user_str = ", ".join([str(x) for x in self.users.all()])
        return "<{}>: {}".format(self.__class__.__name__, user_str)


pre_delete.connect(
    remove_deleted_friend_from_crews,
    sender=Friendship,
    dispatch_uid="remove-deleted-friend-from-crews",
)


class Crew(models.Model):
    """Basically a Facebook Group, for post privacy"""

    name = models.CharField(max_length=100)
    owned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User that made this crew, for their provacy reasons",
        related_name="crews_owned",
    )
    members = models.ManyToManyField(User, related_name="crews_included")

    def __str__(self):
        return "<{}>: {} by {}".format(
            self.__class__.__name__, self.name, self.owned_by
        )
