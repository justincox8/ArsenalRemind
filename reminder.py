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

def next_match(data: dict):
    now = datetime.now()
    fromatted_date_int = int(now.strftime("%Y%m%d"))
    arsenal_matches = []
    filtered_matches = []
    for m in data:
        for i in m["stage"][0]["matches"]:
            if i["teams"]["home"]["name"] == "Arsenal" or i["teams"]["away"]["name"] == "Arsenal":
                arsenal_matches.append(i)
    
    for i in arsenal_matches:
        i["date"] = i["date"].replace("/", "-")
        temp_date = datetime.strptime(i["date"], "%d-%m-%Y")
        temp_format = int(datetime.strftime(temp_date, "%Y%m%d"))

        if temp_format > fromatted_date_int:
            filtered_matches.append(i)

    next_match = filtered_matches[0]
    print(f"{next_match["date"]} {next_match["teams"]["home"]["name"]} vs {next_match["teams"]["away"]["name"]}")
    return next_match

def send_message():
    pass