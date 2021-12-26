from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager, QuerySet, Q, F, Exists


class EventQuerySet(QuerySet):
    def visible_to_user(self, user):
        """
        Return queryset of content objects that are visible to user,
        either bc they created it, or bc privacy of person who creatd it allows them to.
        """
        # user must be:
        #   - in friendship of person who wrote it if there are no visible_to_ s
        # TODO
        #   - if any visible_to_ s are supplied,user must be in selected visible_to clauses
        #   - not in any of the hidden_from
        return self.filter(
            Q(visible_to_friends=None, visible_to_crews=None, user__in=user.friends)
            | Q(user=user)
        )


class EventManager(Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)  # Important!

    def visible_to_user(self, user):
        return self.get_queryset().visible_to_user(user)
