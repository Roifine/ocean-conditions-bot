# TIDE calling and processing script

import arrow
import json
import requests

import os # to load the api keys from my env file
from dotenv import load_dotenv # to load the api keys from my env file

if os.getenv("GITHUB_ACTIONS") is None: # Load environment variables from .env only if running locally
    load_dotenv("api_keys.env")

storm_api = os.getenv("storm_api")  # Now, API_KEY contains "your_secret_key_here"


start = arrow.now().floor('day')
end = arrow.now().shift(days=1).floor('day')

response = requests.get(
  'https://api.stormglass.io/v2/tide/extremes/point', 
  params={
    'lat': -33.8908,
    'lng': 151.2773,
  },
  headers={
    'Authorization': storm_api
  }
)

# Do something with response data.
tide_extreme_data = response.json()



with open("tide_extreme_data.json", "w") as my_file:
    tide_extreme_data = json.dumps(tide_extreme_data, indent=4)
    my_file.write(tide_extreme_data)




response2 = requests.get(
  'https://api.stormglass.io/v2/tide/sea-level/point', 
  params={
    'lat': -33.8908,
    'lng': 151.2773,
  },
  headers={
    'Authorization': storm_api
  }
)



tide_hourly_data = response2.json()

with open("tide_hourly_data.json", "w") as my_file:
    tide_hourly_data = json.dumps(tide_hourly_data, indent=4)
    my_file.write(tide_hourly_data)