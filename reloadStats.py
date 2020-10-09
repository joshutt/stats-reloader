import os
import time

import requests
from dotenv import load_dotenv
from pid import PidFile


def settings():
    load_dotenv()


def make_submission():
    # Run the Update
    r = requests.get(os.getenv("URL"), auth=(os.getenv("USER"), os.getenv("PASSWORD")), verify=False)
    results = r.text
    # print(results)
    if 'Updated Scores' in results:
        return True
    else:
        return False


def main():
    settings()
    sleep_iter = 0
    try:
        base_sec = int(os.getenv("BASE_SECS"))
    except TypeError:
        print("Unable to get BASE_SECS, setting to 60 seconds")
        base_sec = 60
    except ValueError:
        print("BASE_SECS is not a number, setting to 60 seconds")
        base_sec = 60

    with PidFile("statLoad"):
        while sleep_iter < 5:
            success = make_submission()
            if success:
                sleep_iter = 0
            else:
                sleep_iter += 1
            sleep_time = base_sec * 2 ** sleep_iter
            print("Sleep for %d seconds" % sleep_time)
            time.sleep(sleep_time)


if __name__ == '__main__':
    main()
