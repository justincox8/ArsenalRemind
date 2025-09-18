from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import re
import schedule
from chump import Application
from typing import Optional, NamedTuple
import pytz


service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://www.bbc.com/sport/football/teams/arsenal/scores-fixtures")
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

class TodayResult(NamedTuple):
	is_today: bool
	time: Optional[datetime]
	minutes_until_game:Optional[int]

def convert_to_pst(date_obj: datetime, time_str: str)  -> datetime:
	uk_time = datetime.strptime(time_str, "%H:%M")
	uk_time = datetime.combine(date_obj, uk_time.time())
	uk = pytz.timezone("Europe/London")
	pst = pytz.timezone("US/Pacific")
	return uk.localize(uk_time).astimezone(pst)

def countdown(kickoff: datetime, now: Optional[datetime] = None) -> int:
	if now is None:
		now = datetime.now(pytz.timezone("US/Pacific"))	
		return (int(kickoff - now).total_seconds() // 60) 	
def is_today():
	now = datetime.now()
	try:
		date = soup.find("h2")
		date_text = date.get_text(strip=True)
		print(date_text)
		date_clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_text)
		date_clean = f"{date_clean} {now.year}"
		date_obj = datetime.strptime(date_clean, "%A %d %B %Y")
		print(date_obj.date())
		print("this is working")
		if date_obj.date() == now.date():
			return TodayResult(True, None, None)
		else:
			return TodayResult(False, None, None)
	except Exception as e:
		print("parsing failed")
		today_label = soup.find(lambda tag: "Today" in tag.get_text())
		if today_label:
			time_tag = today_label.find_next("time", class_="ssrcss-bkk8ek-StyledTime eli9aj90")
			if time_tag:
				time_str = time_tag.get_text(strip=True)
				print(f"game time found: {time_str}")
				kickoff_pst = convert_to_pst(now.date(), time_str)
				minutes_left = countdown(kickoff_pst, now)
				return TodayResult(True, kickoff_pst, minutes_left)
			return TodayResult(True, None, None)
		return TodayResult(False, None, None)
		
def send_notification(message):
	app = Application("aimfebhb9oc3kc3hdmcuug3z67qh1i")
	client = app.get_user("upoq3r2xg259bb9cr1nwc62mdnd3gm")
	client.send_message(message, title="Arsenal Remind")
	
	


def main():
	result = is_today()
	if result.is_today:
		print("arsenal game today")
		if result.time:
			send_notification(f"Arsenal play in {result.minutes_until_game}")
	else:
		print("there is no game today")
		
	

schedule.every().day.at("08:25").do(main)
while True:
	schedule.run_pending()
	time.sleep(1)
