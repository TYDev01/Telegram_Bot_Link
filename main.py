import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
# Load environment variables from .env
load_dotenv()

# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the keyboard
    url = os.getenv('TELEGRAM_URL')
    url2 = os.getenv('WEBSITE_URL')
    keyboard = [
        [InlineKeyboardButton("Join our Community", url=url)],
        [InlineKeyboardButton("Visit our website", url=url2)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an option:', reply_markup=reply_markup)

# Define the button callback
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Use await here

    if query.data == '1':
        await query.edit_message_text(text="You clicked Button 1")
    elif query.data == '2':
        await query.edit_message_text(text="You clicked Button 2")

def main():
    # Fetch the bot token from the environment
    token = os.getenv("BOT_TOKEN")

    if not token:
        logger.error("Bot token is missing! Make sure it's set in your .env file.")
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Add the command handler for the /start command
    application.add_handler(CommandHandler("start", start))

    # Add the callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button))

    # Log that the bot is starting
    logger.info("Bot is starting...")

    # Start polling for updates and keep the bot running
    application.run_polling()

if __name__ == '__main__':
    main()
