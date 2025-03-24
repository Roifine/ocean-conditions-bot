# this program reads the swell hight stores it and prints it

from datetime import datetime, timedelta # handle time objects
import pytz # handle time zone conversion
import json # handles reading and writting json files
import math

# Function Handling time from UTC to Sydney time
def timezone(time):

    utc_zone = pytz.utc
    sydney_zone = pytz.timezone("Australia/Sydney")

    time = time.replace(tzinfo=utc_zone)
    sydney_time = time.astimezone(sydney_zone)

    return sydney_time

# function to convert speed from meter per second to kilometer per hour and also defines the strength of the wind

def wind_strength(wind_speed_meters_ps: float):
    wind_speed_km_ph = 3.6 * wind_speed_meters_ps
    if wind_speed_km_ph < 10:
        return "Light"
    elif 10 <= wind_speed_km_ph < 20:
        return "Moderate"
    elif 20 <= wind_speed_km_ph:
        return "Strong"

# function to convert degrees to name of swell & wind direction 


def degrees(degree: float):
    if degree >= 330 or degree <= 30:
        return f"North ({degree}°)"
    elif 30 < degree <= 60:
        return f"North East ({degree}°)"
    elif 60 < degree <= 120:
        return f"East({degree}°)"  
    elif 120 < degree <= 150:
        return f"South East ({degree}°)"
    elif 150 < degree <= 210:
        return f"South ({degree}°)"
    elif 210 < degree <= 240:
        return f"South West ({degree})°"
    elif 240 < degree <= 300:
        return f"West ({degree})°"
    elif 300 < degree <= 330:
        return f"North West ({degree})°"
    
# this function would return the effective wind direction for the beach
def effective_wind_direction(wind_direction :float, beach_facing_degree: int):
    if 75 < wind_direction < 155:
        return f"on-shore"
    elif 190 < wind_direction < 270 or 310 < wind_direction < 350:
        return f"off-shore"
    else:
        return f"cross-shore"

def effective_wave_size(size_meter: float, direction: float, period: float):
    size_feet = size_meter / 0.305
    if not 110 < direction < 190:
        size_feet *= 0.6
    if 11 >= period > 8:
        size_feet *= 1.1
    elif period > 11:
        size_feet *= 1.3
    low = math.floor(size_feet)
    high = math.ceil(size_feet)
    return f"{low}-{high}"
      

with open("wave_forecast.json") as wave_file, open("wind_forecast.json") as wind_file :
    wave_data = wave_file.read()
    wind_data = wind_file.read()

surf = json.loads(wave_data) # the whole json file content for wave hight
wind = json.loads(wind_data) # the whole json file content for wind hight


beach_facing_degree = 115 #hard coding to Bondi, this is used in the wind and wave size functions as an input

heights = surf['hours']
wave_dic = {}
for height in heights:
    size_meter = float(height['swellHeight']['sg'])
    direction = float(height['swellDirection']['sg'])
    period = float(height['swellPeriod']['sg'])
    time = timezone(datetime.strptime(height['time'], "%Y-%m-%dT%H:%M:%S%z")) # convert the time into datetime object

    
    wave_dic[time] = {}
    wave_dic[time]['size'] = size_meter 
    wave_dic[time]['direction'] = direction
    wave_dic[time]['period'] = period

       
# loop as the above just for winds json

winds = wind['hours']
for wind in winds:
    wind_direction = float(wind['windDirection']['sg'])
    wind_speed_meters_ps = float(wind['windSpeed']['sg'])
    time = timezone(datetime.strptime(wind['time'], "%Y-%m-%dT%H:%M:%S%z")) # convert the time into datetime object

    wave_dic[time]['wind_direction'] = wind_direction
    wave_dic[time]['wind_speed_km_ph'] = wind_speed_meters_ps 


# printing for 8 am next ten days
today = datetime.today()
end_day = today + timedelta(days=4)

formatted_range = f"{today.day}-{end_day.day}.{today.month}"
print(f"Bondi Surf Forecast {formatted_range}")

count = 0

for time, values in wave_dic.items():
    if time.hour == 8:
        print(f"""
        🌊 {time.strftime("%A")}
        wave size {values['size']}m
        wave direction {(values['direction'])}°
        wave period {(values['period'])}
        wind speed {(values['wind_speed_km_ph'])} 
        wind direction {(values['wind_direction'])}° 
       """)
        count += 1
        if count == 5:
            break
        
       






