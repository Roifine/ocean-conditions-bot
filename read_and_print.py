# this program reads the swell hight stores it and prints it

from datetime import datetime # handle time objects
import pytz # handle time zone conversion
import json # handles reading and writting json files

# Function Handling time from UTC to Sydney time
def timezone(xtime):

    utc_zone = pytz.utc
    sydney_zone = pytz.timezone("Australia/Sydney")

    xtime = xtime.replace(tzinfo=utc_zone)
    sydney_time = xtime.astimezone(sydney_zone)

    return sydney_time

# function to convert speed from meter per second to knots 

def knots(meter: str):
    speed = 1.943844 * int(meter)
    return speed

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
def relative_wind_direction(wind_direction :float, beach_facing_degree: int):
    if beach_facing_degree - 60 < wind_direction < beach_facing_degree + 60:
        return f"Ons-hore"
    elif beach_facing_degree - 95 < wind_direction  < beach_facing_degree -60 or beach_facing_degree + 60 < wind_direction  < beach_facing_degree + 175:
        return f"Cross-shore"
    elif beach_facing_degree - 160 < wind_direction < beach_facing_degree - 95 or beach_facing_degree + 175 < wind_direction  < beach_facing_degree + 200:
        return f"Off-shore"


with open("wave_forecast.json") as wave_file, open("wind_forecast.json") as wind_file :
    wave_data = wave_file.read()
    wind_data = wind_file.read()

surf = json.loads(wave_data) # the whole json file content for wave hight
wind = json.loads(wind_data) # the whole json file content for wind hight


beach_facing_degree = 160 #hard coding to Bondi, this is used in the wind and wave size functions as an input

heights = surf['hours']
wave_dic = {}
for height in heights:
    size = height['swellHeight']['sg']
    direction = height['swellDirection']['sg']
    period = height['swellPeriod']['sg']
    time = datetime.strptime(height['time'], "%Y-%m-%dT%H:%M:%S%z") # convert the time into datetime object

    
    wave_dic[time] = {}
    wave_dic[time]['size'] = size # for the size key in the dictioary add the size as a value in a list of values
    wave_dic[time]['direction'] = degrees(direction)
    wave_dic[time]['period'] = period
       
# loop as the above just for winds json

winds = wind['hours']
for wind in winds:
    wind_direction = float(wind['windDirection']['sg'])
    wind_speed_meters_ph = float(wind['windSpeed']['sg'])
    time = datetime.strptime(wind['time'], "%Y-%m-%dT%H:%M:%S%z") # convert the time into datetime object

    wave_dic[time]['wind_direction'] = relative_wind_direction(wind_direction, beach_facing_degree)
    wave_dic[time]['wind_speed_knots_ph'] = knots(wind_speed_meters_ph) 


# printing for 8 am next ten days

for time, values in wave_dic.items():
    if time.hour == 8:
        print(f"""
        🌊 Surf Report for {time.strftime("%A")}:
        🏄 Wave Height: {round(values['size'], 1)}m
        💨 Wind: {round(values['wind_speed_knots_ph'])} knots from {values['wind_direction']}
        """)
        
       






