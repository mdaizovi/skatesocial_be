from django.contrib import admin
from django.contrib.auth.models import Group

from .models import FriendRequest, Friendship

# Register your models here.

admin.site.register(Friendship)
admin.site.register(FriendRequest)

admin.site.unregister(Group)
