from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from bounty.models import War, Bounty, Message
from users.models import Profile
from django.utils import timezone
from datetime import timedelta
import os
import json

LAMBDA_URL=os.environ.get("LAMBDA_URL")
LAMBDA_API_KEY=os.environ.get("LAMBDA_API_KEY")

@shared_task(name = "check_war_status")
def check_war_status():
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

# CHANGE TO LAMBDA FUNCTION
@shared_task(name='discord_messages')
def discord_messages():
  
    # GET ALL MESSAGES FROM DB AND FORMAT INTO MESSAGES
    all_messages = Message.objects.all()

    message_dict = {}

    for message in all_messages.iterator():
        discordid = message.user.profile.discordid
        
        if message.user.profile.discordmessage:

            if discordid in message_dict:
                message_dict[discordid] += "\n" + message.text
            else:
                message_dict[discordid] = message.text

    # SEND MESSAGES TO LAMBDA HANDLER
    data = { "messages" : message_dict }

    print(data)

    headers = { 
        'Accept':'application/json', 
        "X-API-Key" : LAMBDA_API_KEY, 
        "Connection": "keep-alive"}

    data_string = json.dumps(data)

    print(data_string)

    r = requests.post(url=LAMBDA_URL,json=data_string,headers=headers)

    if (r.status_code == 200):
        all_messages.delete()