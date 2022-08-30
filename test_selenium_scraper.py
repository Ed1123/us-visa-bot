import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from unittest import TestCase

from selenium_scraper import log_in, has_website_changed


class TestSeleniumScraper(TestCase):
    @classmethod
    def get_driver(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        return webdriver.Chrome(options=chrome_options)

    def test_log_in(self):
        sign_in_url = 'file://' + os.path.join(os.getcwd(), 'webpage_checkpoint', 'sign_in_page.html')
        driver = self.get_driver()

        driver.get(sign_in_url)
        log_in(driver)

        driver.quit()

    def test_has_website_changed(self):
        no_appointment_text = 'There are no available appointments at this time.'
        main_page_url = 'file://' + os.path.join(os.getcwd(), 'webpage_checkpoint', 'main_page_appointments_available.html')
        driver = self.get_driver()

        self.assertTrue(has_website_changed(driver, main_page_url, no_appointment_text))

        driver.quit()
