#FireBase
from firebase import info

locationData, sep, tail = info.fetchFromDb().partition(',')

def test_FireBaseHasData():
    assert(locationData != None)
    
def test_FireBaseData():
    assert(isinstance(locationData, str) == True)
