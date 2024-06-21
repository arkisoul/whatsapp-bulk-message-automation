from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import base64
import os

# Load contacts and message
contacts = ["+918655122295", "+918980805858"]  # Add your contacts here
message_text = """💥*गुरुदेव की इस परंपरा को निभा रही सम्पूर्ण भारत की समाज*💥

क्या आपकी समाज ने निभाया अपना दायित्व?

*विगत 55 वर्ष से संघ की परंपरा रही है कि सभी समाज पूज्य गुरुदेव आचार्य भगवन श्री विद्यासागर जी महाराज के चरणों में चातुर्मास का निवेदन करने पंहुचती रही है और गुरुदेव अपनी आज्ञा और संकेत के अनुरूप उपसंघों को चातुर्मास के लिए नगर नगर भिजाते रहे है*

*इस स्वास्थय परंपरा का ध्यान में रखते हुए सभी समाज अपना निवेदन विद्या शिरोमणि आचार्य श्री समय सागर जी महाराज के श्री चरणों में कर रही है। और इस बात के लिए पूर्ण समर्पित है  वह जिस संघ को संकेत करेंगे उन्हीं का चातुर्मास समाज बड़े ही भक्ति भाव से करवाएगी*

हमारा पूर्ण और हमारी पूर्ण समाज का समर्पण गुरुदेव आचार्य श्री विद्यासागर जी महाराज एवं आचार्य श्री समय सागर जी महाराज के लिए है 

निवेदक 
🚩☀️*पुण्योदय विद्यासंघ*🚩☀️"""
# Path to your media file
media_path = "/Users/arpitjain/Downloads/aacharya-parampara.mp4"

# Function to encode media file to base64


def encode_media_to_base64(file_path):
    with open(file_path, "rb") as media_file:
        return base64.b64encode(media_file.read()).decode('utf-8')


# Preload media files into memory
preloaded_media = {
    "media.mp4": encode_media_to_base64(media_path)
}

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH
driver.get("https://web.whatsapp.com")
# Wait for user to scan the QR code
input("Press Enter after scanning QR code")


def send_message(contact, message, media_file=None):
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        )
        search_box.clear()
        search_box.send_keys(contact)
        search_box.send_keys(Keys.ENTER)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        ).send_keys(message + Keys.ENTER)

        if media_file:
            # Decode base64 media file to temp file
            temp_media_path = "/tmp/temp_media.mp4"
            with open(temp_media_path, "wb") as temp_media_file:
                temp_media_file.write(base64.b64decode(
                    preloaded_media[media_file]))

            attach_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[@data-icon='clip']"))
            )
            attach_button.click()

            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(temp_media_path)

            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[@data-icon='send']"))
            )
            send_button.click()

            # Optionally, delete the temp file after sending
            os.remove(temp_media_path)
    except Exception as e:
        print(f"Failed to send message to {contact}: {e}")


# Create and start threads
threads = []

for contact in contacts:
    thread = threading.Thread(target=send_message, args=(
        contact, message_text, "media.mp4"))
    threads.append(thread)
    thread.start()
    time.sleep(1)  # Slight delay to prevent overwhelming the system

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Close the WebDriver
driver.quit()
