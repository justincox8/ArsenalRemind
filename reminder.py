import ntfy
import requests
from dotenv import load_dotenv
import os
import json
from datetime import *
import time
from playwright.sync_api import sync_playwright, Playwright
#make this global so i can use it in other funcitons
load_dotenv()
api_key = os.getenv("API_KEY")


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
    fromatted_date_int = int(now.strftime("%Y%m%d"))
    filtered_matches = []
    arsenal_matches = []
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

def send_message(next_match:dict, h2h:dict):
    message = f"Arsenal play on {next_match["date"]} Match: {next_match["time"]} {next_match["teams"]["home"]["name"]} vs {next_match["teams"]["away"]["name"]} {h2h}"
    with open("screenshots/lineup.png", 'rb') as f:
        requests.post(
            "https://ntfy.sh/ArsenalReminder", 
            data= f, 
            headers={
                "Title": "Arsenal Reminder",
                "Tags": "warning,rotating_light",
                "Priority": "5",
                "Message": message,
                "Filename": "screenshots/lineup.png",
                "Click": f"https://ntfy.sh/ArsenalReminder"

            })

def take_screenshot(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch()
    page = browser.new_page()
    page.goto("https://x.com/Arsenal")
    time.sleep(2)
    page.screenshot(path="screenshots/lineup.png")
    browser.close()