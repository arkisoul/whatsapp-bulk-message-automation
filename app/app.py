# Program to send bulk customized message through WhatsApp web application

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas
import time

# Load the chrome driver
driver = webdriver.Chrome()

# Open WhatsApp URL in chrome browser
driver.get("https://www.google.com")

# sheet_id = '1XqOtPkiE_Q0dfGSoyxrH730RkwrTczcRbDeJJpqRByQ'
# sheet_name = 'sample_1'
# url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

sheet_url = 'https://docs.google.com/spreadsheets/d/1fB1UHWOHXGTWQJ208UEiermUZ6MfOTZpqI_Tea8Vwqw/edit#gid=1484715859'
url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

# Read data from excel
csv_data = pandas.read_csv(url)
np_array = csv_data.to_numpy()

for row in np_array:
    name = row[0]
    number = row[1]
    message = row[2]
    user_url = f'https://web.whatsapp.com/send?phone={number}'
    driver.get(user_url)
    time.sleep(5)
    actions = ActionChains(driver)
    actions.send_keys(message)
    actions.send_keys(Keys.ENTER)
    actions.perform()

# Close chrome browser
driver.quit()
