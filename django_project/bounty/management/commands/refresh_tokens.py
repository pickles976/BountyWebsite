from django.core.management.base import BaseCommand
from users.models import Profile
from django.utils.timezone import timedelta
from django.utils import timezone
import os
import requests

CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")

class Command(BaseCommand):
    help = "Checks the Foxhole WAR API for a new war. If new war has started, all players are un-verified"

    def handle(self, *args, **options):

        profiles = Profile.objects.filter(discordToken__isnull=False)

        age = timedelta(seconds=3)

        for profile in profiles:

            if (timezone.now() - profile.dateAuthorized) > age:

                print(f"Refreshing token for {profile.discordname}")

                try:
                    data = {
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET,
                        'grant_type': 'refresh_token',
                        'refresh_token': profile.refreshToken
                    }
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
                    r.raise_for_status()
                    data = r.json()
                    newToken = data["access_token"]
                    refreshToken = data["refresh_token"]

                    print(data)
                    
                    profile.discordToken = newToken
                    profile.refreshToken = refreshToken
                    profile.save()
                except:
                    profile.discordToken = None
                    profile.refreshToken = None
                    profile.save()