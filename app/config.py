import getpass
import platform

os_name = platform.system()
username = getpass.getuser()

if os_name == 'Darwin':
    CHROME_PROFILE_PATH = f'--user-data-dir=Users/{username}/Library/Application Support/Google/Chrome/WhatsApp'
elif os_name == 'Linux':
    CHROME_PROFILE_PATH = f'--user-data-dir=/home/{username}/.config/google-chrome/WhatsApp'
elif os_name == 'Windows':
    CHROME_PROFILE_PATH = f'--user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\WhatsApp'
