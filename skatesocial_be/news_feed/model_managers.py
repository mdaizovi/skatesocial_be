from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager, QuerySet, Q, F, Exists


class EventQuerySet(QuerySet):
    def visible_to_user(self, user):
        """
        Return queryset of content objects that are visible to user,
        either bc they created it, or bc privacy of person who creatd it allows them to.

        Hierarchy: most specific wins. ie if person is in hidden_from_crews but in visible_to_friends, they can see.
        if friend is in both visible_to_friends and hidden_from_friends, hidden wins.
        """
        # user must be:
        #   - in friendship of person who wrote it if there are no visible_to_ s
        # TODO
        #   - if any visible_to_ s are supplied,user must be in selected visible_to clauses
        #   - not in any of the hidden_from
        # User is not aware of these crews; they belong to other people
        crews_user_is_in = user.crews_included.all()

        basic_privacy = Q(
            visible_to_friends=None,
            visible_to_crews=None,
            hidden_from_friends=None,
            hidden_from_crews=None,
        )
        # reminder & ~Q means "and not"
        crews_included = (
            Q(visible_to_crews__in=crews_user_is_in)
            & ~Q(hidden_from_crews__in=crews_user_is_in)
            & ~Q(hidden_from_friends=user)
        )

        hidden_but_not_from_my_crews = Q(hidden_from_crews__isnull=False) & ~Q(
            hidden_from_crews__in=crews_user_is_in
        )
        hidden_from_my_crew_but_im_visible = Q(
            hidden_from_crews__in=crews_user_is_in
        ) & Q(Q(visible_to_crews__in=crews_user_is_in) | Q(visible_to_friends=user))
        crews_hidden = Q(hidden_but_not_from_my_crews) | Q(
            hidden_from_my_crew_but_im_visible
        )

        return self.filter(Q(user__in=user.friends) | Q(user=user)).filter(
            Q(basic_privacy) | Q(crews_included) | Q(crews_hidden) | Q(user=user)
        )


class EventManager(Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)  # Important!

    def visible_to_user(self, user):
        return self.get_queryset().visible_to_user(user)
