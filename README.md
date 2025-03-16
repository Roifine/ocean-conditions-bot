# super-duper-palm-tree
This Python program runs locally on my Mac and connects to an ocean conditions API to retrieve data for the next 10 days. It's designed to help surfers, swimmers, and snorkelers in Sydney, Australia, by highlighting the best conditions for their activities.
You can access the data with a Telegram bot called SurfReportBot. Look it up on Telegram! https://t.me/OceanReportBot
Files and what they do
**bot.py** - this program, initialize the telegram bot. It serves the info stored and printed in read_and_print.py
**fetch_data.py** - this program fetches the data from the Storm Glass API, 2 requests are called. One for the wave data, size, period and direction. And one for the wind data, speed, and direction
**read_and_print.py** - this program stores the data from the fetch_data file and stores in a dictionary. It has a few functions to simplify the raw data for the user. Lastly, it prints the wave and wind forecast
**telebot.py** - this program initialize the telegram bot and check if it's working
**wave_forecast.json** - this is where the data from the wave api request is stored 
**wind_forecast.json** - this is where the data from the wind api request is stored 
both wave and wind json files need to be triggered manually.

**Next Steps for Improvement:**

- add more data points for better forecast updates, e.g. tide
- build different prints for swimmers, surfers, and snorklers
- build a command and function to print out best days for the user
