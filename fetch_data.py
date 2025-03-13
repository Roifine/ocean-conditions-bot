# this is the file to test how to fetch the data from storm glass API
import json
import requests
###



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
    'Authorization': '7b69f340-fcad-11ef-b19c-0242ac130003-7b69f426-fcad-11ef-b19c-0242ac130003'
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
    'Authorization': '7b69f340-fcad-11ef-b19c-0242ac130003-7b69f426-fcad-11ef-b19c-0242ac130003'
  }
)
###
# Do something with response data.
wind_data = response.json()

#fetching the WIND data



with open("wind_forecast.json", "w") as other_file:
    wind_data = json.dumps(wind_data, indent=4)
    other_file.write(wind_data)
