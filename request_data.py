import requests
import json
import time
import password

data_file = "/data/"

def extract_values(data, key):
    return [x[key] for x in data.values() if key in x]
    
def requestWeatherData(): #requests data from weather.gov, call once every 30 mins and uses the json files
    try:
        api = {"User-Agent": f"Personal use, {password.email}"} #weather.gov requires an API key of what you are doing and your email
        weatherRequest = requests.get("https://api.weather.gov/gridpoints/OKX/24,38",headers=api)
        weather = weatherRequest.json()
    except:
        raise Exception("Could not connect to Weather.gov api")
    try:
        toJSONFile(weather, "weather")
        extractWeatherData()
    except:
        raise Exception("Couldn't extract data from .json")

def extractWeatherData():
    with open(data_file + "weather.json") as f:
        weather = json.load(f)
    humidityData = extract_values(weather, "relativeHumidity")
    temperatureData = extract_values(weather, "temperature")
    try:
        toJSONFile(temperatureData, "temperature")
        toJSONFile(humidityData, "humidity")
    except:
        raise Exception("Couldn't write data to .json")

def toJSONFile(data, name):
    file = data_file +  name + ".json"
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

while True:
    try:
        requestWeatherData()
        print("data pulled")
    except Exception as e:
        print(e)
        pass
    time.sleep(1800) #pulls once every 30 minutes
