from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from bounty.models import War, Bounty, Message
from users.models import Profile
from django.utils import timezone
from datetime import timedelta

@shared_task(name = "check_war_status")
def check_war_status():

    try:

        r = requests.get("https://war-service-live.foxholeservices.com/api/worldconquest/war")
        data = r.json()

        warNumber = data["warNumber"]

        # if the warNumber is greater than the warnumber of the most current war
        currentWar = War.objects.all().latest("pk")
        if warNumber > currentWar.warNumber:

            # SEND MESSAGES ON NEW WAR START
            p = Profile.objects.filter(verified=True,discordmessage=True)
            message = "A new war has started! Visit https://www.foxholebounties.com/profile/ to re-verify with just a click!"

            for profile in p.iterator():

                m = Message(user=profile.user,text=message)
                m.save()

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

    except:
        
        print("Failed to reach server!")

@shared_task(name = "close_old_bounties")
def close_old_bounties():

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