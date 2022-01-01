from itertools import chain
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=50)

    class Meta:
        ordering = ("username", "name")

    @property
    def friends(self):
        qset_list = [u.users.exclude(pk=self.pk) for u in self.friendship_set.all()]
        return list(chain(*qset_list))

    @property
    def email_verified(self):
        email = self.emailaddress_set.filter(primary=True).first()
        return email.verified if email else False
