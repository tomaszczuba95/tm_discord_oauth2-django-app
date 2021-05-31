from django.db import models

# Create your models here.


class DiscordUser(models.Model):
    discord_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now=True)


class TrackmaniaUser(models.Model):
    account_id = models.BigIntegerField(primary_key=True)
    display_name = models.CharField(max_length=100)
    linked_discord = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)
