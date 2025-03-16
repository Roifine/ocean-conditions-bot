from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Define the command function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your OceanReportBot. How can I help you today?')

# Main function to set up the bot
async def main() -> None:
    # Replace your bot token here
    app = Application.builder().token("8188434850:AAGBYgMPghUzu-cc1vlzFjhmjlzXD7lMcSI").build()

    # Add the /start command handler
    app.add_handler(CommandHandler("start", start))

    # Run the bot (this will handle the event loop automatically)
    await app.run_polling()

# Run the bot (Don't call asyncio.run here)
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())  # Just this line remains, which is fine in this case.
