import ntfy
import requests
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo
#make this global so i can use it in other funcitons
load_dotenv()
api_key = os.getenv("API_KEY")
api_football_key = os.getenv("API_FOOTBAL_KEY")
other_comps = os.getenv("OTHER_COMPS_KEY")
champions_league = os.getenv("CHAMPIONS_LEAGUE_ID")
fa_cup = os.getenv("FA_CUP_ID")
efl_cup = os.getenv("EFL_CUP_ID")


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
        i.update({"comp": "prem"})

        if temp_date.date() >= now.date():
            filtered_matches.append(i)
    filtered_matches.append(get_champions_league())
    filtered_matches =  sorted(filtered_matches, key=lambda x: datetime.strptime(x["date"], "%d-%m-%Y"))
    print(filtered_matches)
    for i in filtered_matches[1:]:
        i["time"] = convert_time(i["time"])["string"]
    next_match = filtered_matches[0]
    next_match["time"] = convert_time(next_match["time"])["string"]
    next_match.update({"fixture_list": filtered_matches[1:]})
    
    standings = get_standings()
    next_match.update({"standings": standings})
    with open("data.json", "w") as f:
        json.dump(next_match, f, indent=4)
    return next_match

def check_date(next_match: dict):
    now = datetime.now()
    next_match_date = datetime.strptime(next_match["date"], "%d-%m-%Y")
    if now.date() == next_match_date.date():
        print(f"{next_match["date"]} {next_match["teams"]["home"]["name"]} vs {next_match["teams"]["away"]["name"]}")
        return True
    else:
        print(now.date())
        print(next_match_date.date())
        return False

def convert_time(time):
    gmt = time
   
    today = datetime.now().date()
    
    dt_gmt = datetime.strptime(f"{today} {gmt}", "%Y-%m-%d %H:%M")
    dt_gmt = dt_gmt.replace(tzinfo=ZoneInfo("UTC"))
    
    dt_pacific = dt_gmt.astimezone(ZoneInfo("America/Los_Angeles"))
    dt_string = dt_pacific.strftime("%H:%M")
    return {"time":dt_pacific, "string": dt_string}

def wait_time(nm: dict):

    dt_pacific = nm["time"]
    dt = datetime.strptime(
        f"{nm['date']} {nm['time']}",
        "%d-%m-%Y %H:%M"
    )

    # Attach Pacific timezone (since it's already Pacific time)
    dt_pacific = dt.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
    now = datetime.now(ZoneInfo("America/Los_Angeles"))
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

    headers = {
      'X-Auth-Token': api_football_key,
    }

    response = requests.request("GET", url, headers=headers)
    champ_standings = get_champ_standings()
    data = response.json()
    data.update({"champ": champ_standings})
    return data

def send_message():
    message = f"Arsenal Play in an hour click to see matchup"
    requests.post(
        "https://ntfy.sh/ArsenalReminder",  
        headers={
            "Title": "Arsenal Reminder",
            "Tags": "warning,rotating_light",
            "Priority": "5",
            "Message": message,
            "Click": f"justin.collie-boga.ts.net"

            })

def get_champions_league():
    url = "https://api.football-data.org/v4/competitions/CL/matches"
    
    headers = {
        'X-Auth-Token': api_football_key,
    }
    
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    arsenal_matches = []
    for i in data["matches"]:
        if i["status"] != "FINISHED":
            if i["homeTeam"]["name"] == "Arsenal FC" or i["awayTeam"]["name"] == "Arsenal FC":
               arsenal_matches.append(i) 
    next_match = arsenal_matches[0]
    date = next_match["utcDate"]
    time = date[date.find("T")+1:date.find("Z")-3]
    date = date[:date.find("T")]
    date = datetime.strptime(date, "%Y-%m-%d")
    date = datetime.strftime(date, "%d-%m-%Y")
    next_match.update({"date":date, "time": time})
    next_match.update({"comp": "champ"})
    return next_match

def get_champ_standings():
    url = "https://api.football-data.org/v4/competitions/CL/standings"

    headers = {
      'X-Auth-Token': api_football_key,
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    return data    
data = get_matches()
next_match(data)
