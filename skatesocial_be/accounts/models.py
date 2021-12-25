from itertools import chain
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(unique=True, null=True, blank=True, max_length=50)

    @property
    def friends(self):
        qset_list = [u.users.exclude(pk=self.pk) for u in self.friendship_set.all()]
        return list(chain(*qset_list))
