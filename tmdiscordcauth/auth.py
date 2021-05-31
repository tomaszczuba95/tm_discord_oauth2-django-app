from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser


class DiscordAuthBackend(BaseBackend):
    def authenticate(self, request, user):
        find_user = DiscordUser.objects.filter(discord_id=user['id'])
        if len(find_user) == 0:
            print('User was not found. Saving...')
            new_user = DiscordUser.objects.create_new_discord_user(user)
            print(new_user)
            return new_user
        return find_user
