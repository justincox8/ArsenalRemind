from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import re
import schedule


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
	
	


dates = [tag.text for tag in soup.find_all("time")]

schedule.every().day.at("4:00").do(is_today)
is_today()
while True:
	schedule.run_pending()
	time.sleep(1)

