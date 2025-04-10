# this is the file to test how to fetch the data from storm glass API
import json
import requests
import arrow

import os # to load the api keys from my env file
from dotenv import load_dotenv # to load the api keys from my env file

if os.getenv("GITHUB_ACTIONS") is None: # Load environment variables from .env only if running locally
    load_dotenv("api_keys.env")

STORM_API = os.getenv("STORM_API")  # Now, API_KEY contains "your_secret_key_here"

print(f"STORM_API from env: {os.environ.get('STORM_API')}")

print(f"API Key (raw): '{STORM_API}'")

# Debugging: Check if API Key is loaded (DO NOT print actual key!)
print(f"API key loaded: {'Yes' if STORM_API else 'No'}")  # Debugging only

# Validate API Key before making the request
if not STORM_API:
    raise ValueError("API Key not found! Make sure it's set in the environment variables.")



def write_api_data(json_data: dict, file_name: str):
  errors = json_data.get("errors")
  if errors is None:
    with open(file_name, "w") as my_file:
      json_data = json.dumps(json_data, indent=4)
      my_file.write(json_data)
  else:
    print(errors)
   

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

    'Authorization': STORM_API
  }
)
###
# Do something with response data.
wave_data = response.json()
write_api_data(wave_data, "wave_forecast.json")




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

    'Authorization': STORM_API

  }
)
###
# Do something with response data.
wind_data = response.json()
write_api_data(wind_data, "wind_forecast.json")



start = arrow.now().floor('day')
end = arrow.now().shift(days=1).floor('day')

response = requests.get(
  'https://api.stormglass.io/v2/tide/extremes/point', 
  params={
    'lat': -33.8908,
    'lng': 151.2773,
  },
  headers={
    'Authorization': STORM_API
  }
)

# Do something with response data.
tide_extreme_data = response.json()
write_api_data(tide_extreme_data, "tide_extreme_data.json")







