# from pyvirtualdisplay import Display
from selenium import webdriver
import time
import sys
from telegram import send_message, send_photo
from creds import username, password

def has_website_changed():
    '''Checks for changes in the site. Returns True if a change was found.'''
    # First website
    driver.get('https://ais.usvisa-info.com/en-pe/niv/schedule/32404946/payment')

    # Checking if website is still logged
    print('Logging in.')
    if driver.current_url == 'https://ais.usvisa-info.com/en-pe/niv/users/sign_in':
        # Clicking the first prompt, if there is one
        try:
            driver.find_element_by_xpath(
                '/html/body/div[6]/div[3]/div/button').click()
        except:
            pass
        # Filling the user and password
        user_box = driver.find_element_by_name('user[email]')
        user_box.send_keys(username)
        password_box = driver.find_element_by_name('user[password]')
        password_box.send_keys(password)
        # Clicking the checkbox
        driver.find_element_by_xpath(
            '//*[@id="new_user"]/div[3]/label/div').click()
        # Clicking 'Sign in'
        driver.find_element_by_xpath('//*[@id="new_user"]/p[1]/input').click()
        time.sleep(5)
        # Logging to screen
        print('Logged in.')
    else:
        print('Already logged.')

    print('Checking for changes.')
    no_appointment_text = 'There are no available appointments at this time.'
    main_page = driver.find_element_by_id('main')

    return no_appointment_text not in main_page.text


# To run Chrome in a virtual display.
# display = Display(visible=0, size=(800, 600))
# display.start()


seconds_between_checks = 10 * 60

# Initialize the chromediver (must be installed and in PATH)
driver = webdriver.Chrome()

while True:
    print('Starting a new check.')
    if has_website_changed():
        print('A change was found. Notifying it.')
        send_message('A change was found. Here is an screenshot.')
        # Implement screenshot.
        # Missing get the driver object after checking...
        # send_photo()
        exit()
    else:
        # print(f'No change was found. Checking again in {seconds_between_checks} seconds.')
        # time.sleep(seconds_between_checks)
        for seconds_remaining in range(int(seconds_between_checks), 0, -1):
            sys.stdout.write('\r')
            sys.stdout.write(f'No change was found. Checking again in {seconds_remaining} seconds.')
            sys.stdout.flush()
            time.sleep(1)


# driver.quit()
