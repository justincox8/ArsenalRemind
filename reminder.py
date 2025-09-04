import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from chump import Application
from zoneinfo import ZoneInfo
import time
import sys
import re

url = "https://www.bbc.com/sport/football/teams/arsenal/scores-fixtures"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

def is_today(dt):
	if dt.get_text() == "Today":
		return True
	return False

def get_fixture():
	#get the first time and h2 on page which for bbc in specific will be the soonest games time and date
	date = soup.find("div", {"data-content": "Today"})
	print(date.get_text())

	"""today = datetime.today()
				n = strip_str(date)
				dt = datetime.strptime(n, "%A %d %B")
				dt = dt.replace(year=datetime.today().year, hour=int(time.get_text()[:2]), minute=int(time.get_text()[3:]))"""
	return(date)


def send_notification(message):
	app = Application("aimfebhb9oc3kc3hdmcuug3z67qh1i")
	client = app.get_user("upoq3r2xg259bb9cr1nwc62mdnd3gm")
	client.send_message(message, title="Arsenal Remind")


def main():
	now = datetime.now(ZoneInfo("America/Los_Angeles"))
	dt = get_fixture()
	gtime = soup.find('time').get_text().strip()
	if dt:
		if is_today(dt):
			game_time = datetime.strptime(gtime, "%H:%M")
			game_time = game_time.replace(year=datetime.now().year)
			game_time = game_time.replace(month=datetime.now().month)
			game_time = game_time.replace(day=datetime.now().day)
			game_time_adj = game_time - timedelta(hours=8)
			now =datetime.now()
			time_left = game_time_adj - now
			noitfy_time = time_left.total_seconds() - 900
			print(noitfy_time)
			time.sleep(noitfy_time)
			send_notification(f"Arsenal play in 15 minutes")
		else:
			sys.exit()
	return 0


main()