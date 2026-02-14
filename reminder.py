from arsenal import *
import schedule
import time

def main():
    data = get_matches()
    nm = next_match(data)
    is_today = check_date(nm)
    if(is_today == False):
        wait_time(nm)
        send_message()
    else:
        print("No arsenal game today")

"""schedule.every().day.at("02:45", "America/Los_Angeles").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
"""

main()