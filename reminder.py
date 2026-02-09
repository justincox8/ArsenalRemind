import ntfy
import requests
from dotenv import load_dotenv
import os
import json
from datetime import *




def get_matches():
    load_dotenv()
    api_key = os.getenv("API_KEY")

    #arsneal team id: 3068
    url = "https://api.soccerdataapi.com/matches"
    querystring = {'league_id': 228,'auth_token': api_key}
    headers = {
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data

def check_date(data: dict):
    now = datetime.now()
    fromatted_date = str(now.strftime("%d/%m/%Y"))
    arsenal_matches = []
    for m in data:
        for i in m["stage"][0]["matches"]:
            if i["teams"]["home"]["name"] == "Arsenal" or i["teams"]["away"]["name"] == "Arsenal":
                arsenal_matches.append(i)

    for i in arsenal_matches:
        print(f"{i["date"]} {i["teams"]["home"]["name"]} vs {i["teams"]["away"]["name"]}")