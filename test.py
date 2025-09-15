from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import re
import schedule
from chump import Application


service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://www.bbc.com/sport/football/teams/arsenal/scores-fixtures")
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

def is_today():
	now = datetime.now()
	date = soup.find("h2")
	date_text = date.get_text(strip=True)
	date_clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_text)
	date_clean = f"{date_clean} {now.year}"
	date_obj = datetime.strptime(date_clean, "%A %d %B %Y")
	print(date_obj.date())
	print("this is working")
	return now.date() == date_obj.date()

def send_notification(message):
	app = Application("aimfebhb9oc3kc3hdmcuug3z67qh1i")
	client = app.get_user("upoq3r2xg259bb9cr1nwc62mdnd3gm")
	client.send_message(message, title="Arsenal Remind")
	
	


def main():
	if is_today() == True:
		time = soup.find("time")
		send_message(f"The game is today at {time}")		
	else:
		send_notification("The game is not today")

schedule.every().day.at("04:00").do(main)
while True:
	schedule.run_pending()
	time.sleep(1)

