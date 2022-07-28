import requests
import os 
import json

LAMBDA_URL=os.environ.get("LAMBDA_URL")
LAMBDA_API_KEY=os.environ.get("LAMBDA_API_KEY")

print(LAMBDA_API_KEY,LAMBDA_URL)

data = { 
            "messages" : 
            { 
                "160934795445141504" : "this is an automated message from Lambda triggered by Python" 
            } 
        }

headers = { 
    'Accept':'application/json', 
    "X-API-Key" : LAMBDA_API_KEY, 
    "Connection": "keep-alive"}

data_string = json.dumps(data)

# print(data_string)

r = requests.post(url=LAMBDA_URL,json=data_string,headers=headers)

print(r.status_code)