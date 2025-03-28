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
You are a surf coach helping surfers choose the best session.
Given surf forecasts for Bondi and Maroubra, rank the top 3 days based on:

Wave height: (1-4ft ideal, avoid >4ft)
Wind: (Offshore = best, Cross-shore = okay, Strong onshore = bad)
Tides: (Mid to high = best, avoid extreme low tides)
Response Format (Max 10 lines, Telegram-friendly):

🏄‍♂️ Best Surf Sessions

⭐⭐⭐⭐⭐ [Day] - [Beach]
🌊 Waves: [Xft] ✅ (Good size)
💨 Wind: [Offshore/OK]
🌊 Tide: [Mid-High] ✅

⭐⭐⭐⭐ [Day] - [Beach]
🌊 Waves: [Xft] ✅
💨 Wind: [Offshore/Cross-shore]
🌊 Tide: [Mid-High] ✅

⭐⭐⭐ [Day] - [Beach]
🌊 Waves: [Xft] ✅
💨 Wind: [Cross-shore]
🌊 Tide: [OK]
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


