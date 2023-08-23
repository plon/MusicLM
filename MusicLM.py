import requests 
import os 
import dotenv
import datetime 
import json 
import base64 
import logging 
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver

logging.basicConfig(level=logging.INFO)

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class Music:
    musiclm_url = "https://content-aisandbox-pa.googleapis.com/v1:soundDemo?alt=json"
    url = 'https://aitestkitchen.withgoogle.com/experiments/music-lm'

    def __init__(self):
        self.email = os.environ["EMAIL"]
        self.password = os.environ["PASSWORD"]
        if os.environ["TOKEN"] == "":
            self.token = self.get_token()
        elif self.token_refresh():
            self.token = self.get_token()
        else:
            self.token = os.environ["TOKEN"]

    def get_tracks(self, input, generationCount):
        if not isinstance(generationCount, int):
            generationCount = 2
        generationCount = min(8, max(1, generationCount))

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

        try:
            response = requests.post(self.musiclm_url, headers=headers, data=payload)
        except requests.exceptions.ConnectionError:
            logging.error("Can't connect to the server.")
            # Bad Gateway
            return 502
        if response.status_code == 400:
                logging.error("Oops, can't generate audio for that.")
                # Bad Request
                return 400
        
        tracks = []
        for sound in response.json()['sounds']:
            tracks.append(sound["data"])

        return tracks

    def b64toMP3(self, tracks_list, filename):
        count = 0
        new_filename = filename
        while os.path.exists(new_filename):
            count += 1
            new_filename = f'{filename} ({count})'

        os.mkdir(new_filename)

        for i, track in enumerate(tracks_list):
            with open(f"{new_filename}/track{i+1}.mp3", "wb") as f:
                f.write(base64.b64decode(track))

        logging.info("Tracks successfully generated!")
        # Successful Request
        return 200

    def get_token(self):

        driver = Driver(uc=True, headless=True) 

        try:
            driver.get(self.url)

            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'evTGAR')]"))).click()

                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'lgEhqE')]"))).click()

                driver.switch_to.window(driver.window_handles[1])

                logging.info('Logging in...')
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{self.email}\n')
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{self.password}\n')
                logging.info('Successfully logged in')

                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                logging.ERROR("An error occurred while interacting with the webpage, details: " + str(e))
                raise Exception("Unable to fetch token due to Selenium interaction error")

            sleep(5)
            logging.info('Getting OAuth 2.0 token')
            cookies = driver.get_cookies()

        except Exception as e:
            logging.ERROR("An error occurred while fetching the token, details: " + str(e))
            raise Exception("Unable to fetch token due to browser error")

        finally:
            driver.quit()

        token_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'TOKEN'), None)

        if token_cookie is None:
            raise Exception("Unable to obtain token")

        start_sub = "ya29"
        end_sub = "%22"
        start_idx = token_cookie.index(start_sub)
        end_idx = token_cookie.index(end_sub, start_idx)
        token = token_cookie[start_idx:end_idx]

        dotenv.set_key(dotenv_file, "TOKEN", str(token))
        os.environ["TOKEN"] = str(token)
        dotenv.set_key(dotenv_file, "EXPIRATION_TIMESTAMP", str(datetime.datetime.now() + datetime.timedelta(minutes=59)))
        os.environ["EXPIRATION_TIMESTAMP"] = str(datetime.datetime.now() + datetime.timedelta(minutes=59))

        logging.info('OAuth 2.0 token obtained')
        return token

    def token_refresh(self):
        current_timestamp = datetime.datetime.now().replace(microsecond=0)
        expiration_timestamp = datetime.datetime.strptime(os.environ['EXPIRATION_TIMESTAMP'],  '%Y-%m-%d %H:%M:%S.%f')

        difference = current_timestamp - expiration_timestamp
        if difference >= datetime.timedelta(minutes=0):
            return True
        else:
            return False