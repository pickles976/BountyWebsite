import os 
import json
import time
import discord
import asyncio

PATH = "/tmp/"

def send_messages(users):

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

    DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    client.run(DISCORD_BOT_TOKEN)

def lambda_handler(event,context):

    # this weird double-deserialization is done because of how API-Gateway handles
    # json strings from Python
    print(event)
    data_string=json.loads(event["body"])
    data = json.loads(data_string)["messages"]

    try:
    
        send_messages(data)

        # Hackily reset the asyncio event loop for the next Lambda invocation
        asyncio.set_event_loop(asyncio.new_event_loop())

    except:

        return  {
        'statusCode': 424,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET' 
        },
        'body': "ASYNC ERROR"
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET' 
        },
        'body': "SUCCESS"
    }