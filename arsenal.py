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
api_football_key = os.getenv("API_FOOTBAL_KEY")


def next_match_clean(data: dict):
    nm = data["events"][0]
    nm["strTime"] = convert_time(nm["strTime"])["string"]
    with open("match.json", "w") as f:
        json.dump(nm, f, indent=4)
    return nm
    

def check_date(next_match: dict):
    now = datetime.now()
    next_match_date = datetime.strptime(next_match["dateEvent"], "%Y-%m-%d")
    if now.date() == next_match_date.date():
        print(f"{next_match['dateEvent']} {next_match['strHomeTeam']} vs {next_match['strAwayTeam']}")
        return True
    else:
        print(now.date())
        print(next_match_date.date())
        return False

def convert_time(time):
    gmt = time
   
    today = datetime.now().date()
    
    dt_gmt = datetime.strptime(f"{today} {gmt}", "%Y-%m-%d %H:%M:%S")
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



def get_standings():
        url = "https://api.football-data.org/v4/competitions/PL/standings"
    
        headers = {
          'X-Auth-Token': api_football_key,
        }
    
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        with open("standings.json", "w") as f:
            json.dump(data, f, indent=4)
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


def get_next_match(): 
    url = "https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id=133604"
    headers = {
      'x-apisports-key': other_comps,
    }
    
    response = requests.request("GET", url)
    
    data = response.json()
    with open("other.json", "w") as f:
        json.dump(data, f, indent=4)
    return data
    
def get_previous_match():
    url = "https://www.thesportsdb.com/api/v1/json/123/eventslast.php?id=133604"
    headers = {
      'x-apisports-key': other_comps,
    }
    
    response = requests.request("GET", url)
    
    data = response.json()
    with open("previous.json", "w") as f:
        json.dump(data, f, indent=4)



