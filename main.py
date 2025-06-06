from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import subprocess  # Added to run the external script
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import os # to load the api keys from my env file

from dotenv import load_dotenv # to load the api keys from my env file

import deep_seek

from flask import Flask, jsonify
import threading

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
        await update.message.reply_text("Oi, legend! Hit the blue menu button below to see what’s on offer 🏄‍♂️🤙")
        print("Reply sent")

    async def surf(self, update: Update, context: CallbackContext):

        """Shows the beach selection menu and handles user input."""
        query = update.callback_query

        if query is None:  # If the user just typed /surf, show the menu
            keyboard = [
            [InlineKeyboardButton("Bondi Beach", callback_data="bondi")],
            [InlineKeyboardButton("Maroubra Beach", callback_data="maroubra")]
        ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Choose a beach:", reply_markup=reply_markup)
            return

        await query.answer() # If the user clicked a button, handle their choice
        
        beach = query.data  # "bondi" or "maroubra"
        print(f"User selected {beach}")
        script_file = f"read_and_print_{beach}.py"  # Example: "bondi_forecast.py"

        try:
            result = subprocess.run(["python", script_file], capture_output=True, text=True)
            surf_data = result.stdout.strip() if result.returncode == 0 else f"Error fetching data for {beach.capitalize()}."
        except Exception as e:
            surf_data = f"Error: {e}"

        await query.message.reply_text(f"{beach.capitalize()} Beach\n{surf_data}")

    async def best_waves(self, update: Update, context: CallbackContext):
        """Fetches the best surf days from an external script and sends the result to the user."""
        output = deep_seek.run()
        print(f"User selected best")
        await update.message.reply_text(f"🏄‍♂️ Best Days (8:00 AM):\n\n{output}")


   
    async def on_update_received(self, update: Update, context: CallbackContext):
        msg = update.message
        user = msg.from_user  # Get user info
        print(f"{user.name} wrote: {msg.text}")  # Print user and their message

        # Send a reply to the user (for example, after receiving their message)
        await self.send_text(user.id, f"Oi, {user.name}! Hit the blue menu button below to see what's on offer 🏄‍♂️🤙")
    
    async def send_text(self, chat_id: int, text: str):
        """Send a message to a specific user."""
        try:
            await self.bot.send_message(chat_id=chat_id, text=text)
            print(f"Message sent to {chat_id}: {text}")
        except Exception as e:
            print(f"Error sending message: {e}")

def run_flask():
    from api import app
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
    
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()

    bot = MyBot(token=telegram_api)  # Initialize the bot

    # Create an instance of the Application with your bot's token
    application = Application.builder().token(bot.token).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", bot.start))  # Notice: use 'bot.start' here
    application.add_handler(CommandHandler("forecast", bot.surf))  # Handles /surf 
    application.add_handler(CallbackQueryHandler(bot.surf))
    application.add_handler(CommandHandler("best", bot.best_waves))

    # Register the message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.on_update_received))

    # Run the bot using polling
    application.run_polling()
