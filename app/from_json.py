# Program to send bulk customized message through WhatsApp web application

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
from random import randrange
from os import path
import time
import config
import argparse
import base64
import os

# MESSAGE = """🙏 *आचार्य श्री विद्या सागर जी नमो नम:* 🙏\n🙏 *आचार्य श्री समय सागर जी नमो नम:* 🙏

# मुनि श्री विनम्र सागर जी ससंघ से जुड़ी सूचनाओं के लिए ये नंबर *98261 44235* अपने मोबाइल में save करे

# धन्यवाद\nविनम्रवाणी परिवार इंदौर"""

MESSAGE = """*इंदौर चतुर्मास 2024*

#आचार्यश्रीविद्यासागरजी\r#आचार्यश्रीसमयसागरजी\r#मुनिश्रीविनम्रसागरजी

ऐसा सुंदर अमुख प्रभु का देखते ही रह गए आंखे सबकी झलक गई और प्रभु जी हमको मिल गए सोए भाग जगाए तुमने चारो तीर्थ पा लिया हमने कुछ भी नही काया तुम बिन इसमें प्राण तुम्ही से है ये चमक, ये दमक, फूलवन मा महक सब कुछ सरकार तुम्हई से है"""


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
        self.url = f'https://docs.google.com/spreadsheets/d/{
            self.sheet_id}/export?format=xlsx&gid={self.sheet_gid}'
        self.json_data = None
        self.driver = None
        self.driver_wait = None

    def start_process(self):
        count = 0
        try:
            self.read_data()
            self.load_driver()
            count = self.process_message()
            return count
        finally:
            self.close_driver()

    def read_data(self):
        # Read data from excel
        script_dir = path.dirname(__file__)
        file_rel_path = 'contacts.json'
        file_abs_path = path.join(script_dir, file_rel_path)
        self.json_data = pd.read_json(file_abs_path)

    def load_driver(self):
        # Load the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument(config.CHROME_PROFILE_PATH)
        if config.os_name == 'Windows':
            self.driver = webdriver.Chrome(executable_path=r'C:\Users\Nityam\AppData\Local\Programs\Python\Python39\chromedriver.exe',
                                           options=options)
        else:
            self.driver = webdriver.Chrome(options=options)

        # Open WhatsApp URL in chrome browser
        self.driver.get("https://web.whatsapp.com")
        self.driver_wait = WebDriverWait(self.driver, 10)

    def process_message(self):
        if self.image_path is not None:
            def encode_media_to_base64(file_path):
                with open(file_path, "rb") as media_file:
                    return base64.b64encode(media_file.read()).decode('utf-8')

            # Preload media files into memory
            preloaded_media = {
                "media": encode_media_to_base64(self.image_path)
            }

            # Decode base64 media file to temp file
            temp_media_path = "/tmp/temp_media.mp4"
            with open(temp_media_path, "wb") as temp_media_file:
                temp_media_file.write(base64.b64decode(
                    preloaded_media['media']))

        count = 0
        self.driver.set_page_load_timeout(60)
        # Iterate excel rows till to finish
        contacts = self.json_data.get(0).to_list()
        failed_contacts = []
        for contacts_chunk in np.array_split(contacts, 30):
            for column in contacts_chunk:
                try:
                    # Assign customized message
                    message = MESSAGE

                    # Locate search box through x_path
                    search_box = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div'
                    person_title = self.driver_wait.until(
                        lambda driver: driver.find_element("xpath", search_box))

                    # Clear search box if any contact number is written in it
                    person_title.clear()

                    # Send contact number in search box
                    contact_number = str(column)

                    if len(contact_number) == 10 or not contact_number.startswith('91'):
                        contact_number = '91' + contact_number
                    person_title.send_keys(contact_number)

                    try:
                        # Load error message in case unavailability of contact number
                        self.driver.find_element(
                            "xpath", '//*[@id="pane-side"]/div[1]/div/span')

                        user_url = f'https://web.whatsapp.com/send?phone={
                            contact_number}'
                        self.driver.get(user_url)

                    except NoSuchElementException:
                        person_title.send_keys(Keys.ENTER)

                    time.sleep(2)

                    if self.image_path is not None:
                        attachment_button_path = '//div[@title="Attach"]'
                        attachment_button = self.driver_wait.until(lambda driver: driver.find_element("xpath",
                                                                                                      attachment_button_path))
                        attachment_button.click()
                        image_button_path = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
                        image_button = self.driver_wait.until(
                            lambda driver: driver.find_element("xpath", image_button_path))
                        image_button.send_keys(temp_media_path)
                        # image_button.send_keys(self.image_path)
                        time.sleep(2)
                        self.send_message(message)

                    else:
                        self.send_message(message)
                        # pass

                    timelapse = randrange(1, 2)
                    time.sleep(timelapse)
                    count = count + 1
                except:
                    failed_contacts.append(str(column))

        with open('failed-numbers.txt', 'w') as f:
            f.write(",\n".join(failed_contacts))

        # Optionally, delete the temp file after sending
        if self.image_path is not None:
            os.remove(temp_media_path)

        return count

    def send_message(self, message):
        # Format the message from excel sheet
        # message = message.replace('{customer_name}', str(self.json_data['Name'][count]))
        actions = ActionChains(self.driver)
        message = message.replace("\n", '__new_line__')
        message = message.replace("\r", '__new_line__')
        msg_lines = message.split('__new_line__')
        msg_lines[:] = [msg for msg in msg_lines if msg.strip()]
        for msg in msg_lines:
            actions.send_keys(msg)
            actions.key_down(Keys.SHIFT).key_down(
                Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER)
            actions.key_down(Keys.SHIFT).key_down(
                Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        # Only for sending media
        time.sleep(2)

    def close_driver(self):
        # Close chrome browser
        self.driver.quit()


def main():
    start = time.time()
    count = 0
    print(f'Started at {time.strftime("%Y-%m-%d %H:%M:%S")}')
    try:
        parser = argparse.ArgumentParser(
            description='Whatsapp Bulk Message Automation with optional Attachment feature')
        parser.add_argument(
            '--image-path', help='Full path of image attachment', type=str, dest='image_path')
        parsed_args = parser.parse_args()
        args = vars(parsed_args)
        whatsapp = WhatsappMessage(**args)
        count = whatsapp.start_process()
    except Exception as e:
        print(f'Failed to send message')
        print(e)
    finally:
        end = time.time()
        total = end - start
        total_in_mins = round(total / 60, 2)
        speed = round(count / total_in_mins, 2)
        print(f'Took {total_in_mins} mins to send {
              count} messages at an avg speed of {speed} msg/min')
        print(f'Finished at {time.strftime("%Y-%m-%d %H:%M:%S")}')


if __name__ == '__main__':
    main()
