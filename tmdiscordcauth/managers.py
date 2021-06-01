from django.contrib.auth import models


class DiscordUserAuthManager(models.UserManager):
    def create_new_discord_user(self, user):
        new_user = self.create(
            discord_id=user['id'],
            username=user['username']
        )
        return new_user


class TrackmaniaUserManager(models.UserManager):
    def create_new_trackmania_user(self, request, usertm):
        new_user = self.create(
            account_id=usertm['account_id'],
            display_name=usertm['display_name'],
            linked_discord=request.user
        )
        return new_user
