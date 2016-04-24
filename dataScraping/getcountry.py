#!/usr/bin/env python
import requests
import os

google_api_key = os.getenv('GOOGLE_MAPS_API_KEY')


class GetCountry:

    def getcountry(city):
        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        params = {'address': city,
                  'key': google_api_key}
        data_json = requests.get(url, params).json()
        country = []
        if data_json:
            for entry in data_json['results']:
                country.append(entry['formatted_address'].split(", ")[-1])
            # if len(country) > 1:
            #     country = GetCountry.bestcountry(country)
            #     return country
#            else:
                return country[0]
        else:
            return False

    # def bestcountry(country_list):
    #     country_dict = {}
    #     for country in country_list:
    #         try:
    #             country_dict[country] += 1
    #         except:
    #             country_dict[country] = 1
    #     country_dict = sorted(country_dict.items(),
    #                           key=lambda x: x[1], reverse=True)
    #     return country_dict[0][0]
