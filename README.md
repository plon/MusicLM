# MusicLM

Unofficial reverse engineered API for Google's MusicLM on the AI Test Kitchen

## Dependencies

- Google Chrome
- Python 3.6
- Selenium
- undetected_chromedriver
- python-dotenv
- requests

## Installation

1. Install Python 3 from the official website: https://www.python.org/downloads/
2. Run the following command in your terminal to install the required libraries: 
```sh
pip install selenium undetected-chromedriver python-dotenv requests
```

## Usage

1. Before running the script, make sure you have a Google account that has access to the [AI Test Kitchen](https://aitestkitchen.withgoogle.com/). Join the waitlist [here](https://aitestkitchen.withgoogle.com/signup).
2. Clone the repository and navigate to the directory containing the script.
3. Rename the file `example.env` to `.env` 
4. Store Google sign-in details in the `.env` file (necessary to obtain OAuth2.0 token that is used to generate music)
5. Create a new Python file and import the Music class from the `MusicLM.py` file.
```python
from MusicLM import Music
```
6. Create an instance of the `Music` class.
```python
music = Music()
```
7. Call the `get_music` method on the instance and provide a string input and an integer `generationCount` argument (8 max).
```python
music.get_music("Ambient, soft sounding music I can study to", 2)
```
8. The generated tracks will be saved to a new directory with the same name as the input string.

## How it works

The `Music` class handles authentication using a headless Chrome browser that obtains the OAuth 2.0 authentication token. The `get_token` method logs the user in to the AI Test Kitchen website and retrieves the OAuth 2.0 token from the browser's cookies. The token is saved to a `.env` file. The token expires every hour and is refreshed automatically using the `token_refresh` method.

The `Music` class uses the `requests` library to make a POST request to an API with the input string and the number of tracks to generate. The API returns a JSON object containing the base64-encoded audio data for each track. The base64-encoded audio data is decoded and each track is saved as an MP3 file. 

## Disclaimer

This tool is for educational purposes only and should not be used for any commercial or illegal activities. The author is not responsible for any misuse of this tool.