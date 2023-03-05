# from pyvirtualdisplay import Display
import os
import sys
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from telegram import send_message, send_photo

load_dotenv()
URL_ID = os.getenv('URL_ID')
COUNTRY_CODE = os.getenv('COUNTRY_CODE')
BASE_URL = f'https://ais.usvisa-info.com/en-{COUNTRY_CODE}/niv'


def log_in(driver):
    if driver.current_url != BASE_URL + '/users/sign_in':
        print('Already logged.')
        print(driver.current_url)
        return

    print('Logging in.')

    # Clicking the first prompt, if there is one
    try:
        driver.find_element(By.XPATH, '/html/body/div/div[3]/div/button').click()
    except:
        pass
    # Filling the user and password
    user_box = driver.find_element(By.NAME, 'user[email]')
    user_box.send_keys(os.getenv('USERNAME'))
    password_box = driver.find_element(By.NAME, 'user[password]')
    password_box.send_keys(os.getenv('PASSWORD'))
    # Clicking the checkbox
    driver.find_element(By.XPATH, '//*[@id="sign_in_form"]/div/label/div').click()
    # Clicking 'Sign in'
    driver.find_element(By.XPATH, '//*[@id="sign_in_form"]/p/input').click()

    # Waiting for the page to load.
    # 5 seconds may be ok for a computer, but it doesn't seem enougn for the Raspberry Pi 4.
    time.sleep(10)
    print('Logged in.')


def has_website_changed(driver, url, no_appointment_text):
    '''Checks for changes in the site. Returns True if a change was found.'''
    # Log in
    while True:
        try:
            driver.get(url)
            log_in(driver)
            break
        except ElementNotInteractableException:
            time.sleep(5)

    # # For debugging false positives.
    # with open('debugging/page_source.html', 'w', encoding='utf-8') as f:
    #     f.write(driver.page_source)

    # Getting main text
    main_page = driver.find_element(By.ID, 'main')

    # For debugging false positives.
    with open('debugging/main_page', 'w') as f:
        f.write(main_page.text)

    # If the "no appointment" text is not found return True. A change was found.
    return no_appointment_text not in main_page.text


def run_visa_scraper(url, no_appointment_text):
    # To run Chrome in a virtual display with xvfb (just in Linux)
    # display = Display(visible=0, size=(800, 600))
    # display.start()

    seconds_between_checks = 10 * 60

    # Setting Chrome options to run the scraper headless.
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    if os.getenv('HEADLESS') == 'True':
        chrome_options.add_argument("--headless")  # Comment for visualy debugging

    # Initialize the chromediver (must be installed and in PATH)
    # Needed to implement the headless option
    driver = webdriver.Chrome(options=chrome_options)

    while True:
        current_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
        print(f'Starting a new check at {current_time}.')
        if has_website_changed(driver, url, no_appointment_text):
            print('A change was found. Notifying it.')
            send_message('A change was found. Here is an screenshot.')
            send_photo(driver.get_screenshot_as_png())

            # Closing the driver before quicking the script.
            input('Press enter to quit...')
            driver.close()
            exit()
        else:
            # print(f'No change was found. Checking again in {seconds_between_checks} seconds.')
            # time.sleep(seconds_between_checks)
            for seconds_remaining in range(int(seconds_between_checks), 0, -1):
                sys.stdout.write('\r')
                sys.stdout.write(
                    f'No change was found. Checking again in {seconds_remaining} seconds.'
                )
                sys.stdout.flush()
                time.sleep(1)
            print('\n')


def main():
    base_url = BASE_URL + f'/schedule/{URL_ID}'

    # Checking for an appointment
    url = base_url + '/payment'
    text = 'There are no available appointments at this time.'

    # Checking for a rescheduled
    # url = base_url + '/appointment'
    # text = 'FORCING SCREENSHOT'
    # text = 'There are no available appointments at the selected location.'

    run_visa_scraper(url, text)


if __name__ == "__main__":
    main()
