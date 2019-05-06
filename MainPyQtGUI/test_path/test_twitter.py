#Twitter API Imports
from api import twitterAPI

twitterData = twitterAPI.getTrending()

def test_getTrendingHasData():
    assert(twitterData != None)

def test_getTrendingIsString():
    assert(isinstance(twitterData, str) == True)