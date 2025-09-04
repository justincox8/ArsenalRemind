from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = Options()
options.binary_location = "/usr/bin/chromium"



driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
driver.get("https://www.bbc.com/sport/football/teams/arsenal/scores-fixtures")
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

dates = [tag.text for  tag in soup.find_all("h2")]
print(dates)
driver.quit()
