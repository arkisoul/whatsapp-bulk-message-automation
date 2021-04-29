# Program to send bulk customized message through WhatsApp web application

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import config
import argparse


class WhatsappMessage(object):
    """
    A class that encapsulates Whatsapp Message automation
    function and attributes
    """

    def __init__(self, **kwargs):
        self.sheet_id = kwargs.get('sheet_id')
        self.sheet_name = kwargs.get('sheet_name')
        self.image_path = kwargs.get('image_path')
        self.sheet_gid = kwargs.get('sheet_gid')
        self.url = f'https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=xlsx&gid={self.sheet_gid}'
        self.excel_data = None
        self.driver = None
        self.driver_wait = None

    def start_process(self):
        try:
            self.read_data()
            self.load_driver()
            self.process_message()
        finally:
            self.close_driver()

    def read_data(self):
        # Read data from excel
        self.excel_data = pd.read_excel(self.url, sheet_name=self.sheet_name, engine='openpyxl')

    def load_driver(self):
        # Load the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument(config.CHROME_PROFILE_PATH)
        if config.os_name == 'Windows':
            self.driver = webdriver.Chrome(executable_path=r'C:\Users\Nityam\AppData\Local\Programs\Python\Python39\chromedriver.exe',
                                           options=options)
        self.driver = webdriver.Chrome(options=options)

        # Open WhatsApp URL in chrome browser
        self.driver.get("https://web.whatsapp.com")
        self.driver_wait = WebDriverWait(self.driver, 20)

    def process_message(self):
        count = 0
        # Iterate excel rows till to finish
        for column in self.excel_data['Contact'].tolist():
            # Assign customized message
            message = self.excel_data['Message'][0]

            # Locate search box through x_path
            search_box = '//*[@id="side"]/div[1]/div/label/div/div[2]'
            person_title = self.driver_wait.until(lambda driver: driver.find_element_by_xpath(search_box))

            # Clear search box if any contact number is written in it
            person_title.clear()

            # Send contact number in search box
            contact_number = str(column)
            person_title.send_keys(contact_number)

            # Wait for 2 seconds to search contact number
            time.sleep(2)

            try:
                # Load error message in case unavailability of contact number
                self.driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/span')

                user_url = f'https://web.whatsapp.com/send?phone={contact_number}'
                self.driver.get(user_url)

                # Wait for 5 seconds to load user chat message
                time.sleep(5)

            except NoSuchElementException:
                person_title.send_keys(Keys.ENTER)

            if self.image_path is not None:
                attachment_button_path = '//div[@title="Attach"]'
                attachment_button = self.driver_wait.until(lambda driver: driver.find_element_by_xpath(
                    attachment_button_path))
                attachment_button.click()
                image_button_path = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
                image_button = self.driver_wait.until(lambda driver: driver.find_element_by_xpath(image_button_path))
                image_button.send_keys(self.image_path)
                time.sleep(3)
                self.send_message(message)

            else:
                self.send_message(message)

            time.sleep(1)
            count = count + 1

    def send_message(self, message):
        # Format the message from excel sheet
        # message = message.replace('{customer_name}', str(self.excel_data['Name'][count]))
        actions = ActionChains(self.driver)
        actions.send_keys(message)
        actions.send_keys(Keys.ENTER)
        # actions.perform()
        time.sleep(2)

    def close_driver(self):
        # Close chrome browser
        self.driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Whatsapp Bulk Message Automation with optional Attachment feature')
    parser.add_argument('sheet_id', help='Google Sheet Id', type=str)
    parser.add_argument('sheet_name', help='Google Sheet name', type=str)
    parser.add_argument('sheet_gid', help='Google Sheet gid', type=int)
    parser.add_argument('--image-path', help='Full path of image attachment', type=str, dest='image_path')
    parsed_args = parser.parse_args()
    args = vars(parsed_args)
    whatsapp = WhatsappMessage(**args)
    whatsapp.start_process()
