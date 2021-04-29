# Python Automated Bulk WhatsApp Messages

It is a python script that sends WhatsApp message automatically from WhatsApp web application. It can be configured to send advertising messages to customers. It read data from a Google sheet and send a configured message to people.

## Prerequisites

In order to run the python script, your system must have the following programs/packages installed and the contact number either should be saved in your phone or could be a new number.
* Python >= 3.8: Download it from https://www.python.org/downloads
* Selenium Web Driver: Either you can use repo driver else you can download it https://chromedriver.chromium.org/downloads
* Google Chrome : Download it from https://www.google.com/chrome
* Pandas : Run in command prompt **pip install pandas**
* Xlrd : Run in command prompt **pip install xlrd**
* Openpyxl : Run in command prompt **pip install openpyxl**
* Selenium: Run in command prompt **pip install selenium** 

## Approach
* User scans web QR code to log in into the WhatsApp web application for the new session.
* The script reads a customized message from the Google sheet.
* The script reads rows one by one and searches that contact number in the web search box if the contact number found on WhatsApp then it will send a configured message otherwise it creates url for new number. Then it reads next row. 
* Loop execute until and unless all rows complete.

## Process
* Clone this repository
```commandline
git clone https://github.com/arkisoul/whatsapp-bulk-message-automation
```
* Change directory
```commandline
cd whatsapp-bulk-message-automation
```
* Use any virtualenv for python venv, pipenv, conda and install application dependencies
```commandline
pip install -e requirements.txt
```
* Use below command to send bulk message
    * Without attachment
        ```commandline
        python app/app.py SHEET_ID SHEET_NAME SHEET_GID
        ```
    * With attachment
        ```commandline
        python app/app.py --image-path='absolute/path/to/the/image' SHEET_ID SHEET_NAME SHEET_GID
        ```
    
### Google Sheet Reference
Example Google sheet for your reference
https://docs.google.com/spreadsheets/d/1fB1UHWOHXGTWQJ208UEiermUZ6MfOTZpqI_Tea8Vwqw/edit#gid=1484715859
* Google Sheet ID = 1fB1UHWOHXGTWQJ208UEiermUZ6MfOTZpqI_Tea8Vwqw
* Google Sheet Name = Customers
* Google Sheet Gid = 1484715859

Note: The script may not work in case if the HTML of web WhatsApp is changed.

### Inspiration
This script is inspired from @inforkgodara [repo](https://github.com/inforkgodara/python-automated-bulk-whatsapp-messages) and updated to read a Google sheet and send to any whatsapp number.
