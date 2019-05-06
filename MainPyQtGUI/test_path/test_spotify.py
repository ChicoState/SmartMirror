#Spotify Imports
import urllib.request
import json
from api import spotifyLogIn
import re

spotifyData = spotifyLogIn.get_data()

def test_urlValidation():
    regex = re.compile(r'^(?:http|ftp)s?://', re.IGNORECASE)
    url = spotifyData['item']['album']['images'][0]['url']
    assert(re.match(regex,url) is not None)

def test_spotifyArtist():
    artistInfo = spotifyData['item']['album']['artists'][0]['name']
    assert(isinstance(artistInfo, str) == True)

def test_spotifySongInfo():
    songInfo = spotifyData['item']['name']
    assert(isinstance(songInfo, str) == True)