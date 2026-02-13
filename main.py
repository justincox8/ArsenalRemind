from reminder import *
import schedule
import time

def main():
    data = get_matches()
    nm = next_match(data)
    is_today = check_date(nm)
    if(is_today == True):
        wait_time(nm)
        send_message()
    else:
        print("No arsenal game today")

schedule.every().day.at("03:00", "America/Los_Angeles").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
