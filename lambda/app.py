import os
import requests
import discord
from discord.ext import tasks

URL = "http://foxhole-bounties.herokuapp.com/get_messages"

def request_messages():
    
    headers= { "secret" : os.environ.get("MESSAGE_KEY") }

    r = requests.get(url=URL,headers=headers)

    print(r.json())

    data = r.json()["messages"]

    return data

client = discord.Client()

@client.event
async def on_ready():

    print(f'We have logged in as {client.user}')

    get_messages.start()

@tasks.loop(seconds=30)
async def get_messages(self):
    
    messages = request_messages()

    for user in messages:
        await send_message(user,messages[user])

async def send_message(target,payload):
    try:
        user = await client.fetch_user(target)
        await user.send(payload)
    except:
        print("Could not message user!")

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
client.run(DISCORD_BOT_TOKEN)
