from django.core.management.base import BaseCommand
from bounty.models import Bounty, War
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Checks the Foxhole WAR API for a new war. If new war has started, all players are un-verified"

    def handle(self, *args, **options):

        age = timedelta(days=3)

        # if the warNumber is greater than the warnumber of the most current war
        currentWar = War.objects.all().latest("pk")
        openBounties = Bounty.objects.filter(is_completed=False)

        for bounty in openBounties.iterator():
            if bounty.war.pk != currentWar.pk:
                bounty.is_completed = True
                bounty.save()
            else:
                if (timezone.now() - bounty.date_posted) > age:
                    bounty.is_completed = True
                    bounty.save()