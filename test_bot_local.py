#!/usr/bin/env python3
"""
Local test version of the Telegram bot - no Flask API, just the bot
"""

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import subprocess
import logging
import os
from dotenv import load_dotenv
import deep_seek
import today_analysis

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv("api_keys.env")

telegram_api = os.getenv("TELEGRAM_API") or os.getenv("telegram_api")

class TestBot:
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token=token)

    async def start(self, update: Update, context: CallbackContext):
        print("Received /start command")
        await update.message.reply_text("Oi, legend! Hit the blue menu button below to see what's on offer 🏄‍♂️🤙")
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
        script_file = f"read_and_print_{beach}.py"

        try:
            import sys
            result = subprocess.run([sys.executable, script_file], capture_output=True, text=True)
            surf_data = result.stdout.strip() if result.returncode == 0 else f"Error fetching data for {beach.capitalize()}."
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
            await update.message.reply_text(f"Sorry, couldn't get best waves: {e}")

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

    async def on_update_received(self, update: Update, context: CallbackContext):
        msg = update.message
        user = msg.from_user
        print(f"{user.name} wrote: {msg.text}")
        await update.message.reply_text(f"Oi, {user.name}! Hit the blue menu button below to see what's on offer 🏄‍♂️🤙")

if __name__ == '__main__':
    print("Starting local test bot...")
    
    bot = TestBot(token=telegram_api)
    
    # Create application
    application = Application.builder().token(bot.token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("forecast", bot.surf))
    application.add_handler(CallbackQueryHandler(bot.surf))
    application.add_handler(CommandHandler("best", bot.best_waves))
    application.add_handler(CommandHandler("today", bot.today_surf))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.on_update_received))
    
    print("Bot is running locally. Press Ctrl+C to stop.")
    application.run_polling()