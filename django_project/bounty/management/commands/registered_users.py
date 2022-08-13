from django.core.management.base import BaseCommand
from users.models import Profile
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Consolidates all UserVisit objects into a dailyvisit object"

    def handle(self, *args, **options):

        p = Profile.objects.filter(verified=True)

        profiles = [profile.discordname for profile in p.iterator()]

        print(len(p))
        print(profiles)

