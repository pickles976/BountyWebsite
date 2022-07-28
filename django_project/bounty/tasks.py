from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from bounty.models import War, Bounty, Message
from users.models import Profile
from django.utils import timezone
from datetime import timedelta
import os

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
  
    all_messages = Message.objects.all()

    new_dict = {}

    for message in all_messages.iterator():
        discordid = message.user.profile.discordid
        
        if message.user.profile.discordmessage:

            if discordid in new_dict:
                new_dict[discordid] += "\n" + message.text
            else:
                new_dict[discordid] = message.text

    all_messages.delete()

    DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

    def send_messages(users):

        import time
        import discord

        s = time.time()
        client = discord.Client()

        @client.event
        async def on_ready():

            print(f'We have logged in as {client.user}')
            print(f"{(time.time() - s)*1000}ms elapsed")

            start = time.time()
            for user in users:
                await send_message(user,users[user])
            print(f"{(time.time() - start)*1000}ms elapsed")

            await client.close()

        async def send_message(target,payload):
            try:
                user = await client.fetch_user(target)
                await user.send(payload)
            except:
                print("Could not message user!")

        client.run(DISCORD_BOT_TOKEN)

    send_messages(new_dict)