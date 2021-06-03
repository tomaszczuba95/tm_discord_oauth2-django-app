from rest_framework import serializers
from .models import TrackmaniaUser, DiscordUser


class TrackmaniaUserSerializer(serializers.ModelSerializer):
    #linked_discord = serializers.RelatedField(many=True)

    class Meta:
        model = TrackmaniaUser
        fields = ['account_id', 'display_name', 'linked_discord']
