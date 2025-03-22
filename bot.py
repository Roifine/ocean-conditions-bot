from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import subprocess  # Added to run the external script
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import os # to load the api keys from my env file
from dotenv import load_dotenv # to load the api keys from my env file

if os.getenv("GITHUB_ACTIONS") is None: # Load environment variables from .env only if running locally
    load_dotenv("api_keys.env")

telegram_api = os.getenv("telegram_api")  # Now, API_KEY contains "your_secret_key_here"

class MyBot:
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token=token)

    def run(self):
        # Register handlers and start the bot
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("surf", self.surf_report))  # Added surf command
        self.application.run_polling()

    def get_bot_username(self):
        # You can define a bot username if you wish, or return a placeholder.
        return "OceanReportBot"

    def get_bot_token(self):
        # Returning the token from the bot class
        return self.token
    
    async def start(self, update: Update, context: CallbackContext):
        print("Received /start command")
        await update.message.reply_text("Hello, I'm your bot!")
        print("Reply sent")

    async def surf_report(self, update: Update, context: CallbackContext):
        """Handles /surf command by fetching surf data from an external script."""
        print("Received /surf command")
        try:
            # Run the external script and capture its output
            result = subprocess.run(["python", "read_and_print.py"], capture_output=True, text=True)
            surf_data = result.stdout.strip() if result.returncode == 0 else "Error fetching surf data."
        except Exception as e:
            surf_data = f"Error fetching surf data: {e}"

        await update.message.reply_text(surf_data)  # Send the surf data to the user

    async def on_update_received(self, update: Update, context: CallbackContext):
        msg = update.message
        user = msg.from_user  # Get user info
        print(f"{user.name} wrote: {msg.text}")  # Print user and their message

        # Send a reply to the user (for example, after receiving their message)
        await self.send_text(user.id, f"Thanks for your message {user.name}!")
    
    async def send_text(self, chat_id: int, text: str):
        """Send a message to a specific user."""
        try:
            await self.bot.send_message(chat_id=chat_id, text=text)
            print(f"Message sent to {chat_id}: {text}")
        except Exception as e:
            print(f"Error sending message: {e}")


if __name__ == '__main__':
    bot = MyBot(token=telegram_api)  # Initialize the bot

    # Create an instance of the Application with your bot's token
    application = Application.builder().token(bot.token).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", bot.start))  # Notice: use 'bot.start' here
    application.add_handler(CommandHandler("surf", bot.surf_report))  # Added handler for /surf


    # Register the message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.on_update_received))

    # Run the bot using polling
    application.run_polling()
