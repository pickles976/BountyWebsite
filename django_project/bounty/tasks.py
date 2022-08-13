from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from bounty.models import War, Bounty, Message
from users.models import Profile
from django.utils import timezone
from datetime import timedelta
import os
from users.models import DailyVisit
from user_visit.models import UserVisit


CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")

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
            p = Profile.objects.filter(discordmessage=True)
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

@shared_task(name = "refresh_tokens")
def refresh_tokens():

    profiles = Profile.objects.filter(discordToken__isnull=False)

    age = timedelta(days=3)

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
                profile.dateAuthorized = timezone.now()
                profile.save()
            except:
                profile.discordToken = None
                profile.refreshToken = None
                profile.dateAuthorized = timezone.now()
                profile.save()

@shared_task(name = "log_visits")
def log_visits():

    age = timedelta(days=3)

    visits = UserVisit.objects.filter(created_at__lte=timezone.now()-age)

    visitsDict = {}

    for visit in visits.iterator():

            date = visit.created_at.date()
            
            if date in visitsDict:
                visitsDict[date] += 1
            else:
                visitsDict[date] = 1

    visits.delete()

    print(visitsDict)

    for date in visitsDict:

        try:
            d = DailyVisit.objects.get(date=date)
            d.numVisits += visitsDict[date]
            d.save()
        except:
            v = DailyVisit(date=date,numVisits=visitsDict[date])
            v.save()

@shared_task(name = "test_celery")
def test_celery():

    p = Profile.objects.filter(verified=True).filter(discordmessage=True)
    message = "Celery beat is running"

    for profile in p.iterator():

        m = Message(user=profile.user,text=message)
        m.save()