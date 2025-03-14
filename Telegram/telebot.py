import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Make sure your bot is created correctly
bot = Bot(token="8188434850:AAGBYgMPghUzu-cc1vlzFjhmjlzXD7lMcSI")

async def main():
    # Now this function is asynchronous
    print(await bot.get_me())

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())  # Run the asynchronous function

