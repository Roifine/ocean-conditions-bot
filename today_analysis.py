# Today's AI surf analysis with caching
from datetime import datetime, date, timezone, timedelta
import json
import subprocess
from openai import OpenAI
import os
from dotenv import load_dotenv
import math
import requests

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv("api_keys.env")

deepseek_api = os.getenv("DEEPSEEK_API")
client = OpenAI(api_key=deepseek_api, base_url="https://api.deepseek.com")

def get_wind_description(wind_speed_ms, wind_direction_deg):
    """Convert wind data to descriptive text"""
    # Convert m/s to km/h
    wind_speed_kmh = wind_speed_ms * 3.6
    
    # Determine wind strength
    if wind_speed_kmh < 10:
        strength = "light"
    elif wind_speed_kmh < 20:
        strength = "moderate"
    else:
        strength = "strong"
    
    # For Sydney beaches (east-facing), determine wind direction relative to shore
    # 0-45°: N-NE (offshore to cross-shore)
    # 45-135°: NE-SE (cross-shore to onshore) 
    # 135-225°: SE-SW (onshore to cross-shore)
    # 225-315°: SW-NW (cross-shore to offshore)
    # 315-360°: NW-N (offshore)
    
    if wind_direction_deg < 45 or wind_direction_deg >= 315:
        direction_type = "offshore"
    elif 45 <= wind_direction_deg < 135:
        direction_type = "cross-shore to onshore"
    elif 135 <= wind_direction_deg < 225:
        direction_type = "onshore"
    else:  # 225-315
        direction_type = "cross-shore to offshore"
    
    return f"{int(wind_speed_kmh)}km/h {get_wind_cardinal(wind_direction_deg)} ({strength} {direction_type})"

def get_wind_cardinal(degrees):
    """Convert wind direction degrees to cardinal direction"""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((degrees + 11.25) / 22.5) % 16
    return directions[index]

def interpolate_tide_height(tide_extremes, target_time):
    """Interpolate tide height for a given time based on extreme points"""
    # Find the two extremes that bracket our target time
    before_extreme = None
    after_extreme = None
    
    for extreme in tide_extremes:
        extreme_time = datetime.fromisoformat(extreme['time'].replace('+00:00', ''))
        if extreme_time <= target_time:
            before_extreme = extreme
        elif extreme_time > target_time and after_extreme is None:
            after_extreme = extreme
            break
    
    if not before_extreme or not after_extreme:
        return "na"
    
    # Linear interpolation between the two extremes
    before_time = datetime.fromisoformat(before_extreme['time'].replace('+00:00', ''))
    after_time = datetime.fromisoformat(after_extreme['time'].replace('+00:00', ''))
    
    time_ratio = (target_time - before_time) / (after_time - before_time)
    height_diff = after_extreme['height'] - before_extreme['height']
    interpolated_height = before_extreme['height'] + (height_diff * time_ratio)
    
    # Determine tide direction
    if after_extreme['height'] > before_extreme['height']:
        direction = "rising"
    elif after_extreme['height'] < before_extreme['height']:
        direction = "falling"
    else:
        direction = "steady"
    
    return f"{abs(interpolated_height):.1f}m {direction}"

def fetch_fresh_storm_glass_data():
    """Fetch fresh data from Storm Glass API"""
    import requests
    
    storm_api = os.getenv("STORM_API")
    if not storm_api:
        raise ValueError("STORM_API not found in environment variables")
    
    # Fetch wave data
    wave_response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': -33.8908,
            'lng': 151.2773,
            'params': ','.join(['swellDirection', 'swellHeight', 'swellPeriod']),
            'source': 'sg'
        },
        headers={'Authorization': storm_api}
    )
    
    # Fetch wind data
    wind_response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': -33.8908,
            'lng': 151.2773,
            'params': ','.join(['windDirection', 'windSpeed']),
            'source': 'sg'
        },
        headers={'Authorization': storm_api}
    )
    
    # Fetch tide data
    tide_response = requests.get(
        'https://api.stormglass.io/v2/tide/extremes/point',
        params={
            'lat': -33.8908,
            'lng': 151.2773,
        },
        headers={'Authorization': storm_api}
    )
    
    return wave_response.json(), wind_response.json(), tide_response.json()

def get_today_hourly_forecast():
    """Extract today's hourly forecast data from fresh Storm Glass API data"""
    try:
        # Try to fetch fresh data from API
        try:
            wave_data, wind_data, tide_data = fetch_fresh_storm_glass_data()
            # Check if API returned valid data
            if not wave_data.get('hours') or not wind_data.get('hours'):
                raise ValueError("API returned empty data")
            print("Using fresh API data")
        except Exception as api_error:
            print(f"API fetch failed ({api_error}), falling back to JSON files")
            # Fallback to existing JSON files
            with open('wave_forecast.json', 'r') as f:
                wave_data = json.load(f)
            with open('wind_forecast.json', 'r') as f:
                wind_data = json.load(f)
            with open('tide_extreme_data.json', 'r') as f:
                tide_data = json.load(f)
            print("Using cached JSON data")
        
        # Sydney timezone (UTC+10 standard time in September)
        sydney_tz = timezone(timedelta(hours=10))
        today = date.today()
        
        # Create time range for today 10 AM - 6 PM Sydney time (data available from 10am)
        start_time = datetime.combine(today, datetime.min.time().replace(hour=10)).replace(tzinfo=sydney_tz)
        end_time = datetime.combine(today, datetime.min.time().replace(hour=18)).replace(tzinfo=sydney_tz)
        
        hourly_data = []
        
        # Generate hourly data from 10 AM to 6 PM
        current_time = start_time
        while current_time <= end_time:
            # Convert to UTC for matching with Storm Glass data
            utc_time = current_time.astimezone(timezone.utc)
            time_str = utc_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
            
            # Find matching wave and wind data
            wave_point = next((h for h in wave_data.get('hours', []) if h['time'] == time_str), None)
            wind_point = next((h for h in wind_data.get('hours', []) if h['time'] == time_str), None)
            
            if wave_point and wind_point:
                # Convert wave height from meters to feet
                wave_height_ft = wave_point['swellHeight']['sg'] * 3.28084
                
                # Get wind description
                wind_desc = get_wind_description(
                    wind_point['windSpeed']['sg'],
                    wind_point['windDirection']['sg']
                )
                
                # Get tide information
                tide_info = interpolate_tide_height(tide_data.get('data', []), utc_time.replace(tzinfo=None))
                
                hourly_data.append({
                    'time': current_time.strftime('%I:00 %p'),
                    'wave_height': f"{wave_height_ft:.1f}ft",
                    'wind': wind_desc,
                    'tide': tide_info
                })
            
            current_time += timedelta(hours=1)
        
        return {
            "bondi": hourly_data,
            "maroubra": hourly_data  # Using same data for both beaches for now
        }
        
    except Exception as e:
        print(f"Error reading Storm Glass data: {e}")
        # Fallback to original method if new data isn't available
        return get_today_forecast_data()

def get_today_forecast_data():
    """Get today's forecast by running existing scripts"""
    try:
        # Get the current Python executable path
        import sys
        python_exe = sys.executable
        
        # Run both beach scripts to get today's conditions
        bondi_result = subprocess.run(
            [python_exe, "read_and_print_bondi.py"], 
            capture_output=True, 
            text=True,
            check=True
        )
        
        maroubra_result = subprocess.run(
            [python_exe, "read_and_print_maroubra.py"], 
            capture_output=True, 
            text=True,
            check=True
        )
        
        return {
            "bondi": bondi_result.stdout.strip(),
            "maroubra": maroubra_result.stdout.strip()
        }
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to get forecast data: {e}")

def generate_today_analysis():
    """Generate AI analysis for today's surf conditions"""
    try:
        # Get hourly forecast data
        forecast_data = get_today_hourly_forecast()
        
        # Format hourly data for DeepSeek
        def format_beach_data(beach_data):
            if isinstance(beach_data, list):
                # New hourly format
                formatted_lines = []
                for hour_data in beach_data:
                    formatted_lines.append(
                        f"{hour_data['time']} - Wave: {hour_data['wave_height']}, Wind: {hour_data['wind']}, Tide: {hour_data['tide']}"
                    )
                return "\n".join(formatted_lines)
            else:
                # Fallback to old format
                return str(beach_data)
        
        # Create prompt with hourly data
        user_input = f"""
**Today's Surf Forecast - {date.today().strftime('%A, %B %d')}**

**Bondi Beach:**
{format_beach_data(forecast_data['bondi'])}

**Maroubra Beach:**
{format_beach_data(forecast_data['maroubra'])}
"""
        
        system_prompt = """
You are a professional surf coach analyzing today's surf conditions in Sydney.

The forecast data contains hourly conditions throughout the day. Analyze ALL hours to find the best times.

Format your response exactly like this (use plain text, no ** formatting):

TODAY'S SURF OVERVIEW

Bondi Beach:
- Overall Rating: [Excellent/Good/Fair/Poor]
- Best Times: [list 2-3 specific time windows when conditions are optimal, e.g. "6-8am, 2-4pm"]
- Summary: [2 sentences explaining conditions throughout the day and why these times are best]

Maroubra Beach:
- Overall Rating: [Excellent/Good/Fair/Poor]
- Best Times: [list 2-3 specific time windows when conditions are optimal]
- Summary: [2 sentences explaining conditions throughout the day and why these times are best]

Keep it practical, concise, and based on the actual hourly data provided.
"""
        
        # Call DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )
        
        # Create analysis object
        analysis = {
            "date": date.today().isoformat(),
            "generated_at": datetime.now().isoformat(),
            "analysis": response.choices[0].message.content,
            "raw_forecast": forecast_data
        }
        
        # Save to cache file
        with open("today_analysis.json", "w") as f:
            json.dump(analysis, f, indent=4)
        
        print("Today's AI analysis generated and cached")
        return analysis
        
    except Exception as e:
        print(f"Error generating today's analysis: {e}")
        raise e

def get_cached_today_analysis():
    """Get today's analysis from cache, generate if not exists or outdated"""
    try:
        with open("today_analysis.json", "r") as f:
            cached = json.load(f)
            
        # Check if cache is for today
        if cached["date"] == date.today().isoformat():
            return cached
            
    except FileNotFoundError:
        pass
    
    # Generate new analysis
    return generate_today_analysis()

if __name__ == "__main__":
    # Test the analysis generation
    analysis = generate_today_analysis()
    print("\n" + "="*50)
    print("TODAY'S AI SURF ANALYSIS")
    print("="*50)
    print(analysis["analysis"])