from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import subprocess  # Added to run the external script
import sys
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import os # to load the api keys from my env file

from dotenv import load_dotenv # to load the api keys from my env file

import deep_seek
import today_analysis
import tomorrow_analysis

from flask import Flask, jsonify
import threading

# Check if running in production (Railway sets these)
is_production = any([
    os.getenv("GITHUB_ACTIONS"),
    os.getenv("RAILWAY_ENVIRONMENT"), 
    os.getenv("RAILWAY_PROJECT_ID"),
    os.getenv("PORT")  # Railway typically sets PORT
])

if not is_production:  # Load environment variables from .env only if running locally
    load_dotenv("api_keys.env")

telegram_api = os.getenv("TELEGRAM_API") or os.getenv("telegram_api")  # Check both uppercase and lowercase

# Debug environment variables
print(f"Environment check:")
print(f"is_production: {is_production}")
print(f"GITHUB_ACTIONS: {os.getenv('GITHUB_ACTIONS')}")
print(f"RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT')}")
print(f"RAILWAY_PROJECT_ID: {os.getenv('RAILWAY_PROJECT_ID')}")
print(f"PORT: {os.getenv('PORT')}")
print(f"TELEGRAM_API loaded: {bool(telegram_api)}")
if telegram_api:
    print(f"TELEGRAM_API starts with: {telegram_api[:10]}...")
print(f"Available env vars: {[k for k in os.environ.keys() if not k.startswith('_')]}")

if not telegram_api:
    raise ValueError("TELEGRAM_API environment variable not found! Check Railway environment variables.")


class MyBot:
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token=token)
        self.application = Application.builder().token(token).build()

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
            import sys
            result = subprocess.run([sys.executable, script_file], capture_output=True, text=True, timeout=30)
            surf_data = result.stdout.strip() if result.returncode == 0 else f"Error fetching data for {beach.capitalize()}."
        except subprocess.TimeoutExpired:
            surf_data = "Request timed out. Please try again."
        except Exception as e:
            surf_data = f"Error: {e}"

        await query.message.reply_text(f"{beach.capitalize()} Beach\n{surf_data}")

    async def best_waves(self, update: Update, context: CallbackContext):
        """Fetches the best surf days from an external script and sends the result to the user."""
        try:
            output = deep_seek.run()
            print(f"User selected best")
            await update.message.reply_text(f"🏄‍♂️ Best Days (8:00 AM):\n\n{output}")
        except Exception as e:
            print(f"Error in best_waves: {e}")
            await update.message.reply_text(f"Sorry, couldn't get best waves forecast: {e}")

    async def today_surf(self, update: Update, context: CallbackContext):
        """Fetches today's AI surf analysis and sends it to the user."""
        try:
            print(f"User requested today's analysis - starting...")
            analysis = today_analysis.get_cached_today_analysis()
            print(f"Analysis retrieved successfully")
            await update.message.reply_text(f"🏄‍♂️ {analysis['analysis']}")
            print(f"Message sent to user")
        except Exception as e:
            print(f"Error in today_surf: {e}")
            await update.message.reply_text(f"Sorry, couldn't get today's analysis: {e}")

    async def tomorrow_surf(self, update: Update, context: CallbackContext):
        """Fetches tomorrow's AI surf analysis and sends it to the user."""
        try:
            print(f"User requested tomorrow's analysis - starting...")
            analysis = tomorrow_analysis.get_cached_tomorrow_analysis()
            print(f"Analysis retrieved successfully")
            await update.message.reply_text(f"🏄‍♂️ {analysis['analysis']}")
            print(f"Message sent to user")
        except Exception as e:
            print(f"Error in tomorrow_surf: {e}")
            await update.message.reply_text(f"Sorry, couldn't get tomorrow's analysis: {e}")


   
    async def on_update_received(self, update: Update, context: CallbackContext):
        msg = update.message
        user = msg.from_user  # Get user info
        print(f"{user.name} wrote: {msg.text}")  # Print user and their message

        # Only respond to non-command messages
        if not msg.text.startswith('/'):
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
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Initialize the bot
    bot = MyBot(token=telegram_api)
    
    # Register handlers
    bot.application.add_handler(CommandHandler("start", bot.start))
    bot.application.add_handler(CommandHandler("forecast", bot.surf))
    bot.application.add_handler(CallbackQueryHandler(bot.surf))
    bot.application.add_handler(CommandHandler("best", bot.best_waves))
    bot.application.add_handler(CommandHandler("today", bot.today_surf))
    bot.application.add_handler(CommandHandler("tomorrow", bot.tomorrow_surf))
    bot.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.on_update_received))
    
    print("Bot starting...")
    # Run the bot
    bot.application.run_polling(drop_pending_updates=True)
