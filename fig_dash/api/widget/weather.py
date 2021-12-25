import json
import parse
import requests
from typing import Union


class WeatherData:
    '''structure of the weather data.'''
    def __init__(self, json):
        pass


class WeatherEngine:
    '''convenience class to interact with wttr.in'''
    def __init__(self):
        # history of fetched information.
        self.history = []

    def get_nearest_area(self, data: Union[None, dict]=None):
        area = {}
        if data is None:
            data = self.history[-1]
        data = data["nearest_area"][0]
        area["coords"] = (data['latitude'], data['longitude'])
        area["area"] = data["areaName"][0]['value']
        area["region"] = data["region"][0]['value']
        area["country"] = data["country"][0]['value']
        area["population"] = data["population"]
        area["weather_url"] = data["weatherUrl"][0]['value']

        return area

    def get_current_condition(self, data: Union[None, dict]=None):
        current_condition = {}
        if data is None:
            data = self.history[-1]
        data = data["current_condition"][0]
        current_condition["feels_like"] = {
            "C": data["FeelsLikeC"],
            "F": data["FeelsLikeF"],
        }
        current_condition["humidity"] = data["humidity"]
        current_condition["datetime"] = data["localObsDateTime"]
        current_condition["cloud_cover"] = data["cloudcover"]
        current_condition["observed_at"] = data["observation_time"]
        current_condition["precipitation"] = {
            "mm": data["precipInches"],
            "inch": data["precipMM"],
        }
        current_condition["pressure"] = {
            ".": data["pressure"],
            "inches": data["pressureInches"],
        }
        current_condition["temp"] = {
            "C": data["temp_C"],
            "F": data["temp_F"],
        }
        current_condition["uv"] = data["uvIndex"]
        current_condition["visibility"] = {   
            ".": data["visibility"],
            "miles": data["visibilityMiles"],
        }
        current_condition["code"] = data["weatherCode"]
        current_condition["desc"] = data["weatherDesc"][0]['value']
        current_condition["icon_url"] = data["weatherIconUrl"][0]['value']
        current_condition["wind"] = {
            "deg": data["winddirDegree"],
            "dir": data["winddir16Point"],
            "speed": data["windspeedKmph"],
            "speed_miles": data["windspeedMiles"],
        }

        return current_condition

    def get_lat_lon(self, data: Union[None, dict]=None):
        '''
        Get the latitude and longitude info from the weather JSON response. 
        returns tuple of (lat, lon)
        '''
        if data is None:
            data = self.history[-1]
        request = data["request"][0]
        if request["type"] != "LatLon":
            return (None, None)

        return tuple(parse.parse("Lat {} and Lon {}", request["query"]))

    def build_query(self, region=None, version=2):
        query = "wttr.in"
        if version == 2:
            query = "v2." + query
        if region is not None:
            query += f"/{region}"
        else:
            query += "/"

        return f"https://{query}?format=j1"

    def __call__(self, **args):
        # request weather for a specific region.
        region = args.get("region")
        version = args.get("version", 2)
        query = self.build_query(region=region, version=version)
        try:
            data = json.loads(requests.get(query).text)
            self.history.append(data)
            return data
        except:
            print("error occured in fetching data.")
        

        
        