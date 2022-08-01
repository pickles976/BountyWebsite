import requests
from django.core.management.base import BaseCommand, CommandError
from bounty.models import War, Message
from users.models import Profile

class Command(BaseCommand):
    help = "Checks the Foxhole WAR API for a new war. If new war has started, all players are un-verified"

    def handle(self, *args, **options):
        r = requests.get("https://war-service-live.foxholeservices.com/api/worldconquest/war")
        data = r.json()

        warNumber = data["warNumber"]

        # if the warNumber is greater than the warnumber of the most current war
        currentWar = War.objects.all().latest("pk")
        if warNumber > currentWar.warNumber:

            # unverify all user profiles
            Profile.objects.all().update(verified=False)

            # save the winner and times of this war
            currentWar.winner = data["winner"]
            currentWar.startTime = data["conquestStartTime"]
            currentWar.endTime = data["conquestEndTime"]
            currentWar.save()

            # create new war object with data
            war = War(warNumber=warNumber,winner="NONE")
            war.save()