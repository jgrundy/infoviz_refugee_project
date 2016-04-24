import os
import requests


def CountryToCity(city):
    google_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {'address': city,
              'key': google_api_key}
    data_json = requests.get(url, params).json()
    if data_json:
        for entry in data_json['results']:
            return entry['formatted_address'].split(', ')[-1]
