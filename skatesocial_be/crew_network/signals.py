def remove_deleted_friend_from_crews(sender, **kwargs):
    friendship = kwargs["instance"]
    for u in friendship.users.all():
        other_friend = friendship.users.exclude(pk=u.pk).first()
        for crew in u.crews_owned.all():
            if other_friend in crew.members.all():
                crew.members.remove(other_friend)
