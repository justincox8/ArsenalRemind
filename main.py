from reminder import *

def main():
    data = get_matches()
    nm = next_match(data)
    with sync_playwright() as playwright:
        take_screenshot(playwright)
    send_message(nm)


main()
