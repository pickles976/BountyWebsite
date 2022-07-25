from django.core.management.base import BaseCommand
from bounty.models import Message
import os

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

class Command(BaseCommand):
    help = "Gets all messages from database and sends them to users through Discord"

    def handle(self, *args, **options):
        
        all_messages = Message.objects.all()

        new_dict = {}

        for message in all_messages.iterator():
            discordid = message.user.profile.discordid

            if discordid in new_dict:
                new_dict[discordid] += "\n" + message.text
            else:
                new_dict[discordid] = message.text

        Message.objects.all().delete()
        send_messages(new_dict)

