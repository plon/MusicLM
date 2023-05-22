from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import requests
from time import sleep
import os 
import dotenv
import datetime
import json
import base64

class Music:

    
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    musiclm_url = "https://content-aisandbox-pa.googleapis.com/v1:soundDemo?alt=json"
    url = 'https://aitestkitchen.withgoogle.com/experiments/music-lm'

    def __init__(self):
        self.CHROME_EXE_PATH = None
        self.email = os.environ["EMAIL"]
        self.password = os.environ["PASSWORD"]
        self.browser_executable_path = self.get_chrome_exe_path()
        if os.environ["TOKEN"] == "":
            self.token = self.get_token()
        elif self.token_refresh():
            self.token = self.get_token()
        else:
            self.token = os.environ["TOKEN"]

    def get_music(self, input, generationCount):
        if type(generationCount) != int:
            generationCount = 2
        if generationCount > 8:
            generationCount = 8
        if generationCount < 1:
            generationCount = 1

        payload = json.dumps({
        "generationCount": generationCount,
        "input": {
            "textInput": input
        },
        "soundLengthSeconds": 30  # this doesn't change anything 
        })

        headers = {
        'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("POST", self.musiclm_url, headers=headers, data=payload)
        if response.status_code == 400:
            print("Oops, can't generate audio for that.")
            return
        
        tracks = []
        for sound in response.json()['sounds']:
            tracks.append(sound["data"])

        if os.path.exists(input):
            count = 1

            while os.path.exists(input + " (" + str(count) + ")"):
                count += 1

            os.mkdir(input + " (" + str(count) + ")")
            input = input + " (" + str(count) + ")"
        else:
            os.mkdir(input)

        for i, track in enumerate(tracks):
            with open(f"{input}/track{i+1}.mp3", "wb") as f:
                f.write(base64.b64decode(track))

        print("Tracks successfully generated!")
    
    def get_token(self):
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = uc.Chrome(options = chrome_options, use_subprocess=True, browser_executable_path=self.broser_executable_path) 
        wait = WebDriverWait(driver, 20)

        driver.get(self.url)

        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'ktZYzZ')]"))).click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'lgEhqE')]"))).click()

        driver.switch_to.window(driver.window_handles[1])
        
        print('Logging in...')
        wait.until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{self.email}\n')
        wait.until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{self.password}\n')
        print('Successfully logged in')

        driver.switch_to.window(driver.window_handles[0])
    
        sleep(5)
        print('Getting OAuth 2.0 token')
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'TOKEN':
                token_cookie = cookie['value']
                break
        
        start_sub = "ya29"
        end_sub = "%22"
        start_idx = token_cookie.index(start_sub)
        end_idx = token_cookie.index(end_sub, start_idx)
        token = token_cookie[start_idx:end_idx]

        dotenv.set_key(self.dotenv_file, "TOKEN", str(token))
        dotenv.set_key(self.dotenv_file, "EXPIRATION_TIMESTAMP", str(datetime.datetime.now() + datetime.timedelta(minutes=59)))

        print('OAuth 2.0 token obtained')
        return token

    def token_refresh(self):
        current_timestamp = datetime.datetime.now().replace(microsecond=0)
        expiration_timestamp = datetime.datetime.strptime(os.environ['EXPIRATION_TIMESTAMP'],  '%Y-%m-%d %H:%M:%S.%f')

        difference = current_timestamp - expiration_timestamp
        if difference >= datetime.timedelta(minutes=59):
            return True
        else:
            return False
        
    def get_chrome_exe_path(self):
        if self.CHROME_EXE_PATH is not None:
            return self.CHROME_EXE_PATH
        # linux pyinstaller bundle
        chrome_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome', "chrome")
        if os.path.exists(chrome_path):
            if not os.access(chrome_path, os.X_OK):
                raise Exception(f'Chrome binary "{chrome_path}" is not executable. '
                                f'Please, extract the archive with "tar xzf <file.tar.gz>".')
            CHROME_EXE_PATH = chrome_path
            return CHROME_EXE_PATH
        # windows pyinstaller bundle
        chrome_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome', "chrome.exe")
        if os.path.exists(chrome_path):
            CHROME_EXE_PATH = chrome_path
            return CHROME_EXE_PATH
        # system
        CHROME_EXE_PATH = uc.find_chrome_executable()
        return CHROME_EXE_PATH