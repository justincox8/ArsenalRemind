import ntfy
import requests
from dotenv import load_dotenv
import os
import json
from datetime import *
import time
from datetime import datetime
from zoneinfo import ZoneInfo

#make this global so i can use it in other funcitons
load_dotenv()
api_key = os.getenv("API_KEY")
api_football_key = os.getenv("API_FOOTBAL_KEY")


def get_matches():
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
    filtered_matches = []
    arsenal_matches = []
    for m in data:
        for i in m["stage"][0]["matches"]:
            if i["teams"]["home"]["name"] == "Arsenal" or i["teams"]["away"]["name"] == "Arsenal":
                arsenal_matches.append(i)
    
    for i in arsenal_matches:
        i["date"] = i["date"].replace("/", "-")
        temp_date = datetime.strptime(i["date"], "%d-%m-%Y")

        if temp_date.date() > now.date():
            filtered_matches.append(i)
    for i in filtered_matches[1:]:
        i["time"] = convert_time(i["time"])["string"]
    next_match = filtered_matches[0]
    next_match["time"] = convert_time(next_match["time"])["string"]
    next_match.update({"fixture_list": filtered_matches[1:]})
    with open("next_match.json", "w") as f:
        json.dump(next_match, f, indent=4)
    return next_match

def check_date(next_match: dict):
    now = datetime.now()
    next_match_date = datetime.strptime(next_match["date"], "%d-%m-%Y")
    if now.date() == next_match_date.date():
        print(f"{next_match["date"]} {next_match["teams"]["home"]["name"]} vs {next_match["teams"]["away"]["name"]}")
        return True
    else:
        return False

def convert_time(time):
    gmt = time
    now = datetime.now(ZoneInfo("America/Los_Angeles"))
    today = datetime.now().date()
    
    dt_gmt = datetime.strptime(f"{today} {gmt}", "%Y-%m-%d %H:%M")
    dt_gmt = dt_gmt.replace(tzinfo=ZoneInfo("UTC"))
    
    dt_pacific = dt_gmt.astimezone(ZoneInfo("America/Los_Angeles"))
    dt_string = dt_pacific.strftime("%H:%M")
    return {"time":dt_pacific, "string": dt_string}

def wait_time(nm: dict):
    dt_pacific = convert_time(nm["time"])["time"]

    difference = (dt_pacific - now).total_seconds() - 4500
    
    time.sleep(difference)

def head_to_head(next_match: dict):
    home = next_match["teams"]["home"]["id"]
    away = next_match["teams"]["away"]["id"]
    url = "https://api.soccerdataapi.com/head-to-head"
    querystring = {'team_1_id': home, 'team_2_id': away,'auth_token': api_key}
    headers = {
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    return data

def get_standings():
    url = "https://api.football-data.org/v4/competitions/PL/standings"

    payload={'league': 39, 'season': 2025}
    headers = {
      'X-Auth-Token': api_football_key,
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)

def send_message():
    message = f"Arsenal Play in an hour click to see matchup"
    requests.post(
        "https://ntfy.sh/ArsenalReminder",  
        headers={
            "Title": "Arsenal Reminder",
            "Tags": "warning,rotating_light",
            "Priority": "5",
            "Message": message,
            "Click": f"https://ntfy.sh/ArsenalReminder"

            })


