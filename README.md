### Working 09/06/23

# MusicLM

Unofficial API for Google's MusicLM on the AI Test Kitchen

## Dependencies

- Google Chrome
- Python >= 3.6
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
7. Call the `get_tracks` method on the instance and provide a string input and an integer `generationCount` argument (8 max).
```python
input = "Ambient, soft sounding music I can study to"
tracks = music.get_tracks(input, 2)
```
8. Call the `base64toMP3` method on the instance and provide the returned tracks from the `get_tracks` method and a filename.
```python
music.base64toMP3(tracks, input)
```
9. The generated tracks will be saved to a new directory with the same name as the input string.

## How it works

The `Music` class handles authentication using a headless Chrome browser that obtains the OAuth 2.0 authentication token. The `get_token` method logs the user in to the AI Test Kitchen website and retrieves the OAuth 2.0 token from the browser's cookies. The token is saved to a `.env` file. The token expires every hour and is refreshed automatically using the `token_refresh` method.

The `Music` class uses the `requests` library to make a POST request to an API with the input string and the number of tracks to generate. The API returns a JSON object containing the base64-encoded audio data for each track. The base64-encoded audio data is decoded with the `base64toMP3` method and each track is saved as an MP3 file. 

## Filter Bypass ("Oops, can't generate audio for that.")

Normally if you input popular media references, it returns an error inferring that it can't generate it (presumably due to copyright issues)

But simply enclosing the references `<>` bypasses it for some reason and works as expected, like here the output music is an unmistakable combination of Attack on Titan's OST's time signature & instruments and the dramatic undertone of Dark Souls OST.

https://github.com/armintum/MusicLM/assets/115377622/8f50ee22-d8cb-4370-93ee-343e2aa66db3


This bypass was discovered and shared by [ArpanTripathi](https://twitter.com/ArpanTripathi20) on Twitter

 https://twitter.com/ArpanTripathi20/status/1661292475892285441

## Disclaimer

This tool is for educational purposes only and should not be used for any commercial or illegal activities. The author is not responsible for any misuse of this tool.

## Errors


 ```OsError: [WinError 6] The handle is invalid```  - refer to this issue: https://github.com/ultrafunkamsterdam/undetected-chromedriver/pull/1256

