from openai import OpenAI
import os # to load the api keys from my env file
import subprocess
from dotenv import load_dotenv # to load the api keys from my env file

if os.getenv("GITHUB_ACTIONS") is None: # Load environment variables from .env only if running locally
    load_dotenv("api_keys.env")

deepseek_api = os.getenv("deepseek_api")  # Now, API_KEY contains "your_secret_key_here"

client = OpenAI(api_key=deepseek_api, base_url="https://api.deepseek.com")

# Step 1: Run your existing scripts and capture their output
def get_forecast(script_name):
    result = subprocess.run(
        ["python", script_name], 
        capture_output=True, 
        text=True,
        check=True
    )

    return result.stdout

bondi_forecast = get_forecast("read_and_print_bondi.py")
maroubra_forecast = get_forecast("read_and_print_maroubra.py")

# Step 2: Combine forecasts into a single prompt
user_input = f"""
**Bondi Forecast**
{bondi_forecast}

**Maroubra Forecast**
{maroubra_forecast}
"""


system_prompt = """
You are a surf coach helping beginners choose the best surf session. 
Given surf forecasts for Bondi and Maroubra, rank the top 3 days/times to surf based on:
- Wave height (beginners need 1-4ft)
- Wind (offshore = best, cross/onshore = okay, strong/moderate onshore = bad)
- Tides (mid, high tide often best)

**Response Format:**
1. **Best Day/Beach**  
   🏄 [Wave height]  
   💨 [Wind]  
   🌊 [Best time based on tides]  
   ⭐ [Rating: 5 (best) to 1 (bad)]  

2. **Second Best**  
   (Same format)  

3. **Third Best**  
   (Same format)  

**Avoid:**  
- Days with waves >4ft (dangerous for beginners)  
- Strong onshore winds  
Make sure you write the result in a way that would be user friendly and visual friendly in a telegram bot app. Finish with good surf wishes but never ask a question
"""

def run():
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        stream=False
    )

    return response.choices[0].message.content


if __name__ == 'main':
    run()


