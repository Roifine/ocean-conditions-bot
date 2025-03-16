# super-duper-palm-tree
This project is using Python and run locally on my Mac
This code connects to ocean conditions API and retrive the conditions for the next 10 days. I am looking to build some cool functions to highlight the best conditions for surfers, swimmers, and snorklers.
At the moment, I only fetch the conditions for Synday Australia
You can access the data with a Telegram bot called SurfReportBot. Look it up on Telegram! 
Files and what they do
bot.py - this program, initialize the telegram bot. It serves the info stored and printed in read_and_print.py
fetch_data.py - this program fetches the data from the Storm Glass API, 2 requests are called. One for the wave data, size, period and direction. And one for the wind data, speed, and direction
read_and_print.py - this program stores the data from the fetch_data file and stores in a dictionary. It has a few functions to simplify the raw data for the user. Lastly, it prints the wave and wind forecast
telebot.py - this program initialize the telegram bot and check if it's working
wave_forecast.json - this is where the data from the wave api request is stored 
wind_forecast.json - this is where the data from the wind api request is stored 
