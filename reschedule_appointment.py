from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import sys
from telegram import send_message, send_photo
from creds import username, password
from selenium_scraper import log_in


url = 'https://ais.usvisa-info.com/en-pe/niv/schedule/32404946/appointment'

# Setting Chrome options to run the scraper headless.
chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")

# Initialize the chromediver (must be installed and in PATH)
# Needed to implement the headless option
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()


def check_for_appointments():
    '''Checks for changes in the site. Returns True if a change was found.'''
    # First website
    driver.get(url)

    # Logging in
    log_in()

    print('Checking for changes.')
    no_appointment_text = 'There are no available appointments at this time.'
    main_page = driver.find_element_by_id('main')

    print(main_page.text)
    # return no_appointment_text not in main_page.text


def repeat_check(seconds_between_checks):
    '''A function that calls the checking function in a given interval of time'''
    while True:
        current_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
        print(f'Starting a new check at {current_time}.')
        if check_for_appointments():
            print('A change was found. Notifying it.')
            send_message('A change was found. Here is an screenshot.')
            # Implement screenshot.
            # Missing get the driver object after checking...
            # send_photo()
            exit()
        else:
            #
            for seconds_remaining in range(int(seconds_between_checks), 0, -1):
                sys.stdout.write('\r')
                sys.stdout.write(
                    f'No change was found. Checking again in {seconds_remaining} seconds.')
                sys.stdout.flush()
                time.sleep(1)
            print('\n')


if __name__ == "__main__":
    repeat_check(seconds_between_checks=5 * 60)
