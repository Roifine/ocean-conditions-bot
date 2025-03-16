import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import os # to load the api keys from my env file
from dotenv import load_dotenv # to load the api keys from my env file

if os.getenv("GITHUB_ACTIONS") is None: # Load environment variables from .env only if running locally
    load_dotenv("api_keys.env")

telegram_api = os.getenv("telegram_api")  # Now, API_KEY contains "your_secret_key_here"

# Make sure your bot is created correctly
bot = Bot(token=telegram_api)

async def main():
    # Now this function is asynchronous
    print(await bot.get_me())

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())  # Run the asynchronous function

