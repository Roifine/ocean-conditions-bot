# this program reads the swell hight stores it and prints it

from datetime import datetime, timedelta # handle time objects
import pytz # handle time zone conversion
import json # handles reading and writting json files
import math

# Function Handling time from UTC to Sydney time
def timezone(xtime):

    utc_zone = pytz.utc
    sydney_zone = pytz.timezone("Australia/Sydney")

    xtime = xtime.replace(tzinfo=utc_zone)
    sydney_time = xtime.astimezone(sydney_zone)

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
    
def compass_add(a, b):
    result = (a + b) % 360
    return result if result >= 0 else result + 360


def degrees(degree: float): # Currently not in use! function to convert degrees to name of swell & wind direction 
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

def effective_wave_size(size_meter: float, direction: float, period: float, beach_facing_degree: float):
    size_feet = size_meter / 0.305
    if not beach_facing_degree + 45 > direction > beach_facing_degree - 45:
        size_feet *= 0.7
    if 11 > period > 8:
        size_feet *= 1.1
    elif period >= 11:
        size_feet *= 1.2
    low = math.floor(size_feet)
    high = math.ceil(size_feet)
    if low != high:
        return f"{low}-{high}"
    else:
        return f"{low}-{high+1}"


def find_closest_tides(tide_calander, target_time="8:00", days_ahead=5):
    # Convert target_time from string to datetime.time object
    reference_time = datetime.strptime(target_time, "%H:%M").time()
    # Dictionary to store results
    tide_summary = {}
    # Get today's date
    today = datetime.now().date()
    # Loop through the next `days_ahead` days
    for day_offset in range(days_ahead):
        target_date = today + timedelta(days=day_offset)

        # Get all tide data for the target date
        tides_for_day = tide_calander.get(target_date, [])

        # Variables to track the closest tides before and after target_time
        closest_before = None
        closest_after = None

        for tide in tides_for_day:
            tide_time = tide['tide_time'].time()  # Extract time only

            if tide_time < reference_time:
                closest_before = tide  # Update latest before target_time
            elif tide_time > reference_time and closest_after is None:
                closest_after = tide  # Set first after target_time

        # Store the results for the day
        tide_summary[target_date] = {
            'before': closest_before,
            'after': closest_after
        }
    return tide_summary
      

with open("wave_forecast.json") as wave_file, open("wind_forecast.json") as wind_file, open("tide_extreme_data.json") as tide_extreme_file :
    wave_data = wave_file.read()
    wind_data = wind_file.read()
    tide_extreme = tide_extreme_file.read()

surf = json.loads(wave_data) # the whole json file content for wave hight
wind = json.loads(wind_data) # the whole json file content for wind hight
tide_extreme = json.loads(tide_extreme)



beach_facing_degree = 145 #hard coding to Bondi, this is used in the wind and wave size functions as an input
heights = surf['hours']
wave_dic = {}
for height in heights:
    size_meter = float(height['swellHeight']['sg'])
    direction = float(height['swellDirection']['sg'])
    period = float(height['swellPeriod']['sg'])
    time = timezone(datetime.strptime(height['time'], "%Y-%m-%dT%H:%M:%S%z")) # convert the time into datetime object

    
    wave_dic[time] = {}
    wave_dic[time]['size'] = effective_wave_size(size_meter, direction, period, beach_facing_degree) # for the size key in the dictioary add the size as a value in a list of values
    wave_dic[time]['direction'] = degrees(direction)
    wave_dic[time]['period'] = period

       
# loop as the above just for winds json

winds = wind['hours']
for wind in winds:
    wind_direction = float(wind['windDirection']['sg'])
    wind_speed_meters_ps = float(wind['windSpeed']['sg'])
    time = timezone(datetime.strptime(wind['time'], "%Y-%m-%dT%H:%M:%S%z")) # convert the time into datetime object and use the timezone function to convert to sydney time

    wave_dic[time]['wind_direction'] = effective_wind_direction(wind_direction, beach_facing_degree)
    wave_dic[time]['wind_speed_km_ph'] = wind_strength(wind_speed_meters_ps) 


# with the tides info, i'm gonna create a dictionry, indide it would be a list of dictionaries
tide_calander = {}
extremes = tide_extreme['data']
for tide_extreme in extremes:
    tide_time = timezone(datetime.strptime(tide_extreme['time'], "%Y-%m-%dT%H:%M:%S%z"))
    tide_type = tide_extreme['type']
    tide_height = tide_extreme['height']

    tide_key = tide_time.date() # here I'm createing the key of the dictionary which is the date
    if tide_key not in tide_calander: # i'm ensuring i'm not overriding with a new list if a key already exists
        tide_calander[tide_key] = [] # i'm creating a list for each date key
    tide_calander[tide_key].append({ # i'm adding a dictionary to the list
        'tide_time' : tide_time,
        'type' : tide_type, 
        'height' : tide_height
        })


#for key_wave, value in wave_dic.items():
    #print(f" in {key_wave} the tide is {wave_dic[key_wave]['tide_level']} and the tide extremes that day are {wave_dic[key_wave]['tides'][0]}{wave_dic[key_wave]['tides'][1]}")
today = datetime.today()
end_day = today + timedelta(days=4)


tide_results = find_closest_tides(tide_calander, "08:00", days_ahead=6)

formatted_range = f"{today.day}-{end_day.day}.{today.month}"
print(f"{formatted_range} 8:00 AM")


count = 0

for time, values in wave_dic.items():
    if time.hour == 8:
        date = time.date() # Extract the date from time
        tide_info = tide_results.get(date, {}) # Get tide info for this day
        # Extract before and after tide details
        before_tide = tide_info.get('before')
        after_tide = tide_info.get('after')
        # Check if before_tide exists before trying to use it
        if before_tide:
            before_tide_msg = f"{before_tide['type']} at {before_tide['tide_time'].strftime('%H:%M')}"
        else:
            before_tide_msg = "na"

        # Check if after_tide exists before trying to use it
        if after_tide:
            after_tide_msg = f"{after_tide['type']} at {after_tide['tide_time'].strftime('%H:%M')}"
        else:
            after_tide_msg = "No tide after 8 AM"

        print(f"""
        🗓️ {time.strftime("%A")}
        🏄 {values['size']} ft
        💨 {values['wind_speed_km_ph']} {values['wind_direction']} wind
        🌊 Tides: {before_tide_msg}, {after_tide_msg}
       """)
        count += 1
        if count == 5:
            break
        
       






