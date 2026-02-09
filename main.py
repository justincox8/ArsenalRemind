from reminder import *

def main():
    data = get_matches()
    nm = next_match(data)
    send_message(nm)
    return 0


main()
