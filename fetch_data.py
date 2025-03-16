# this is the file to test how to fetch the data from storm glass API
import json
import requests

import os # to load the api keys from my env file
from dotenv import load_dotenv # to load the api keys from my env file

if os.getenv("GITHUB_ACTIONS") is None: # Load environment variables from .env only if running locally
    load_dotenv("api_keys.env")

storm_api = os.getenv("storm_api")  # Now, API_KEY contains "your_secret_key_here"


# fetching the WAVES data
response = requests.get(
  'https://api.stormglass.io/v2/weather/point',
  params={
    'lat': -33.8908,
    'lng': 151.2773,
    'params': ','.join(['swellDirection', 'swellHeight', 'swellPeriod']),
    'source': 'sg'
  },
  headers={

    'Authorization': storm_api
  }
)
###
# Do something with response data.
wave_data = response.json()


with open("wave_forecast.json", "w") as my_file:
    wave_data = json.dumps(wave_data, indent=4)
    my_file.write(wave_data)


#fetching the WIND data



response = requests.get(
  'https://api.stormglass.io/v2/weather/point',
  params={
    'lat': -33.8908,
    'lng': 151.2773,
    'params': ','.join(['windDirection', 'windSpeed']),
    'source': 'sg'
  },
  headers={

    'Authorization': storm_api

  }
)
###
# Do something with response data.
wind_data = response.json()

#fetching the WIND data



with open("wind_forecast.json", "w") as other_file:
    wind_data = json.dumps(wind_data, indent=4)
    other_file.write(wind_data)
