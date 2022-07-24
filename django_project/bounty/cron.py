import requests
# from bounty.models import War
# from users.models import Profile

def check_war_api():

    r = requests.get("https://war-service-live.foxholeservices.com/api/worldconquest/war")
    data = r.json()

    warNumber = data["warNumber"]

    # if the warNumber is greater than the warnumber of the most current war

    # create new war object with data