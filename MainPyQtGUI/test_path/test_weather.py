#Weather Imports
from api import weather

icon, temp, tempScale, location ,localizedName \
        = weather.get_weather()

def test_validateIconData():
    assert(isinstance(icon, int) == True)

def test_validateTemperatureData():
    assert(isinstance(temp, int) == True)

def test_validateTempScaleData():
    assert(tempScale == '°F')

def test_validateLocationData():
    assert(isinstance(location, str) == True)

def test_validateLocationNameData():
    assert(isinstance(localizedName, str) == True)