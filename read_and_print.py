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

# openning the wave hights file


with open("wave_forecast.json") as wave_file, open("wind_forecast.json") as wind_file :
    wave_data = wave_file.read()
    wind_data = wind_file.read()

surf = json.loads(wave_data) # the whole json file content for wave hight
wind = json.loads(wind_data) # the whole json file content for wind hight

# the following loop takes the wave hight, direction, and period for Bondi and prints them for every day in the next 10 days at 8 am 

heights = surf['hours']
wave_dic = {}
for height in heights:
    size = height['swellHeight']['sg']
    direction = height['swellDirection']['sg']
    period = height['swellPeriod']['sg']
    time = datetime.strptime(height['time'], "%Y-%m-%dT%H:%M:%S%z") # convert the time into datetime object

    
    wave_dic[time] = {}
    wave_dic[time]['size'] = size # for the size key in the dictioary add the size as a value in a list of values
    wave_dic[time]['direction'] = direction
    wave_dic[time]['period'] = period
       
# loop as the above just for winds json

winds = wind['hours']
for wind in winds:
    wind_direction = wind['windDirection']['sg']
    wind_speed = wind['windSpeed']['sg']
    time = datetime.strptime(wind['time'], "%Y-%m-%dT%H:%M:%S%z") # convert the time into datetime object

    wave_dic[time]['wind_direction'] = wind_direction
    wave_dic[time]['wind_speed'] = wind_speed 


# printing for 8 am next ten days

for time, values in wave_dic.items():
    if time.hour == 8:
        print(f"{time.strftime("%A")} {time.hour}:00 - {round(values['size'], 1)} meters. Swell direction is {round(values['direction'])} with {round(values['period'])} seconds period. Wind is {values['wind_speed']} from {values['wind_direction']} {values['wind_speed']} ")
       
# Now I'm going to print the wind direction and speed for each day at 8 
#winds = wind['hours']
#for wind in winds['hours']:







# later I'd like to combine the wind and wave hight into one message



