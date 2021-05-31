from django.contrib.auth import models


class DiscordUserAuthManager(models.UserManager):
    def create_new_discord_user(self, user):
        new_user = self.create(
            discord_id=user['id'],
            username=user['username']
        )
        return new_user
