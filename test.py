from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://www.bbc.com/sport/football/teams/arsenal/scores-fixtures")
time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

dates = [tag.text for tag in soup.find_all("time")]

print(dates)

driver.quit()
