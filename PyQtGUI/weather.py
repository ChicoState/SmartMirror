import json
import time
import urllib.request
from config import YOUR_API

def get_weather():

    accuweatherApiKey = YOUR_API
    location_id = "Chico"
    locationKey = " "

    locationResourceURL = 'https://dataservice.accuweather.com/locations/v1/cities/search?apikey=' + accuweatherApiKey + '&q=' + location_id;
    data = " "

    with urllib.request.urlopen(locationResourceURL) as url:
        location_data = json.loads(url.read().decode())
        locationKey = location_data[0]["Key"]


    currentConditionsResourceURL = 'https://dataservice.accuweather.com/currentconditions/v1/' + locationKey + '?apikey=' + accuweatherApiKey + '&details=true';

    with urllib.request.urlopen(currentConditionsResourceURL) as url:
        weather_data = json.loads(url.read().decode())
        data = weather_data

    tempScale = '°F'
    return (data[0]['WeatherIcon'], round(data[0]['Temperature']['Imperial']['Value']), tempScale, location_id, location_data[0]['AdministrativeArea']['LocalizedName'])
