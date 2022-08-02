from distutils.log import info
import requests

def getUserInfoFromToken(access_token):

    # GET USER AND GUILD INFO
    infoDict = {}

    response = requests.get("https://discord.com/api/v6/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    infoDict["user"] = response.json()

    response = requests.get("https://discordapp.com/api/users/@me/guilds", headers={"Authorization": f"Bearer {access_token}"})
    infoDict["guilds"] = response.json()

    return infoDict