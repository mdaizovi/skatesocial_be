from django.contrib import admin
from django.contrib.auth.models import Group

from .models import FriendRequest, Friendship, Crew

# Register your models here.

admin.site.register(Friendship)
admin.site.register(FriendRequest)
admin.site.register(Crew)

admin.site.unregister(Group)
