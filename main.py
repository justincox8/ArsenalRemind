from reminder import *

def main():
    data = get_matches()
    nm = next_match(data)
    h2h = head_to_head(nm)
    with sync_playwright() as playwright:
        take_screenshot(playwright)
    send_message(nm, h2h)


main()
