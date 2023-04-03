import requests
from cfg import API_TOKEN


def get_city_coords(city):
    params = {
        'q': city,
        'appid': API_TOKEN,
    }
    response = requests.get('https://api.openweathermap.org/geo/1.0/direct', params=params)
    if response.json():
        lat = response.json()[0].get('lat')
        lon = response.json()[0].get('lon')
        return lat, lon
    else:
        return None, None


def get_weather(lat, lon):
    if lat is not None and lon is not None:
        params = {
            'appid': API_TOKEN,
            'lat': lat,
            'lon': lon,
            'lang': 'ru',
            'units': 'metric',
        }
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params).json()
        temp = response.get('main').get('temp')
        wind = response.get('wind').get('speed')
        city = response.get('name')
        description = response.get('weather')[0].get('description')
        return {
            'temp': int(temp),
            'wind': wind,
            'city': city,
            'description': description,
        }
    else:
        return None
