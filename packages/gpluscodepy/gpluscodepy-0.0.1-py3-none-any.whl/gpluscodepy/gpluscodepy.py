import json
import re
import requests
import datetime
import time
import openlocationcode.openlocationcode as olc

class Converter:
    def __init__(self, api_key, index=[]):
        self.cities = index
        self.ratelimit = 0.1
        self.api_key = api_key
        self.lastcall = datetime.datetime.now()

    def getCities(self):
        return self.cities

    def decode(self, pluscode):
        match = re.match('^(\S*\+\S{2})\s*(.*?)$', pluscode)
        fullcode = None
        if match is not None:
            if match.group(2) != "":
                fullcode = self.convertShortcodeToFull(match.group(1), match.group(2))
            else:
                fullcode = pluscode
        if not fullcode:
            return False
        try:
            decoded = olc.decode(fullcode)
        except:
            return False
        return (decoded.latitudeCenter, decoded.longitudeCenter)

    def convertShortcodeToFull(self, pluscode, place):
        city = [item for item in self.cities if item['name'] == place]
        if len(city) == 0:
            time_diff = datetime.datetime.now() - self.lastcall
            time_diff = time_diff.total_seconds()
            time_diff = self.ratelimit-time_diff
            time.sleep(time_diff if time_diff > 0 else 0)
            city = self.getNewData(place)
            if city is False: return False
            print(f'fetching coordinates for {place}')
            self.cities = self.cities + [city]
        else:
            city = city.pop()
        city_prefix = olc.encode(city['latitude'], city['longitude'])[0:4]
        return f'{city_prefix}{pluscode}'

    def getNewData(self, place):
        if place == "": return False
        city = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={
                'key': self.api_key,
                'address': place
            })
        self.lastcall = datetime.datetime.now()
        city = city.json()['results'].pop(0)
        return {'name': place, 'latitude': float(city['geometry']['location']['lat']), 'longitude': float(city['geometry']['location']['lng'])}