from django.contrib import admin
from .models import DiscordUser, TrackmaniaUser

# Register your models here.


@admin.register(DiscordUser)
class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ('discord_id', 'username', 'last_login')


@admin.register(TrackmaniaUser)
class TrackmaniaUserAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'display_name', 'linked_discord')
