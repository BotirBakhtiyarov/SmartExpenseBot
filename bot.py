"""
Main Telegram bot file for SmartExpenseBot.
Initializes bot, handlers, and scheduler.
"""

import telebot
from telebot import types
import signal
import sys
import logging
from telebot import apihelper
from config import Config
from database import Database
from scheduler import ReminderScheduler
from handlers.expense_handler import ExpenseHandler
from handlers.report_handler import ReportHandler
from handlers.reminder_handler import ReminderHandler
from handlers.settings_handler import SettingsHandler
from handlers.about_handler import AboutHandler
from keyboards import create_main_keyboard, create_language_keyboard
from translations import get_translation, get_language_name

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure proxy if provided (optional)
if Config.PROXY_URL:
    apihelper.proxy = {'https': Config.PROXY_URL}
    logger.info(f"Using proxy: {Config.PROXY_URL}")
else:
    # No proxy configured - use direct connection
    apihelper.proxy = None
    logger.info("No proxy configured - using direct connection")

# Validate configuration
try:
    Config.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    sys.exit(1)

# Initialize bot
bot = telebot.TeleBot(Config.BOT_TOKEN)

# Initialize database
db = Database()

# Initialize scheduler first (needed by reminder handler)
scheduler = ReminderScheduler(bot, db)

# Initialize handlers
expense_handler = ExpenseHandler(bot, db)
report_handler = ReportHandler(bot, db)
reminder_handler = ReminderHandler(bot, db)
settings_handler = SettingsHandler(bot, db)
about_handler = AboutHandler(bot, db)

# Pass scheduler to reminder handler for scheduling new reminders
reminder_handler.scheduler = scheduler

# User states: {user_id: "expense" | "report" | "reminder" | "settings" | "none"}
user_states = {}


# Start command
@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    """Handle /start command."""
    user = db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
    language = user.language or "en"
    
    # Request location if timezone is not set
    if not user.timezone or user.timezone == 'UTC':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard.add(types.KeyboardButton(get_translation(language, "share_location"), request_location=True))
        keyboard.add(types.KeyboardButton(get_translation(language, "skip")))
        
        if language == "en":  # First time user
            bot.reply_to(
                message,
                get_translation("en", "welcome") + "\n\n" + get_translation("en", "request_location_for_timezone"),
                reply_markup=keyboard
            )
        else:
            bot.reply_to(
                message,
                get_translation(language, "request_location_for_timezone"),
                reply_markup=keyboard
            )
        return
    
    if language == "en":  # First time user
        bot.reply_to(
            message,
            get_translation("en", "welcome"),
            reply_markup=create_language_keyboard()
        )
    else:
        bot.reply_to(
            message,
            get_translation(language, "main_menu"),
            reply_markup=create_main_keyboard(language)
        )


# Language selection callback
@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def language_callback(call: telebot.types.CallbackQuery):
    """Handle language selection."""
    language_code = call.data.split("_")[1]
    db.update_user_language(call.from_user.id, language_code)
    user_states[call.from_user.id] = "none"
    
    # Get updated user
    user = db.get_or_create_user(call.from_user.id, call.from_user.first_name or "User")
    language = user.language or "en"
    
    bot.answer_callback_query(call.id)
    
    # Request location if timezone is not set
    if not user.timezone or user.timezone == 'UTC':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard.add(types.KeyboardButton(get_translation(language, "share_location"), request_location=True))
        keyboard.add(types.KeyboardButton(get_translation(language, "skip")))
        
        bot.send_message(
            call.message.chat.id,
            get_translation(language, "request_location_for_timezone"),
            reply_markup=keyboard
        )
        return
    bot.send_message(
        call.message.chat.id,
        get_translation(language_code, "language_set"),
        reply_markup=create_main_keyboard(language_code)
    )


# Main menu button handlers
@bot.message_handler(func=lambda message: message.text and (
    get_translation("en", "expenses") in message.text or
    get_translation("ru", "expenses") in message.text or
    get_translation("uz", "expenses") in message.text
))
def expenses_button(message: telebot.types.Message):
    """Handle expenses button."""
    expense_handler.handle_expense_command(message)
    user_states[message.from_user.id] = "expense"


@bot.message_handler(func=lambda message: message.text and (
    get_translation("en", "reports") in message.text or
    get_translation("ru", "reports") in message.text or
    get_translation("uz", "reports") in message.text
))
def reports_button(message: telebot.types.Message):
    """Handle reports button."""
    report_handler.handle_report_command(message)
    user_states[message.from_user.id] = "report"


@bot.message_handler(func=lambda message: message.text and (
    get_translation("en", "reminders") in message.text or
    get_translation("ru", "reminders") in message.text or
    get_translation("uz", "reminders") in message.text
))
def reminders_button(message: telebot.types.Message):
    """Handle reminders button."""
    reminder_handler.handle_reminder_command(message)
    user_states[message.from_user.id] = "reminder"


@bot.message_handler(func=lambda message: message.text and (
    get_translation("en", "settings") in message.text or
    get_translation("ru", "settings") in message.text or
    get_translation("uz", "settings") in message.text
))
def settings_button(message: telebot.types.Message):
    """Handle settings button."""
    # Exit any active modes
    expense_handler.active_expense_mode.discard(message.from_user.id)
    report_handler.active_report_mode.discard(message.from_user.id)
    reminder_handler.active_reminder_mode.discard(message.from_user.id)
    user_states[message.from_user.id] = "none"
    settings_handler.handle_settings_command(message)


@bot.message_handler(func=lambda message: message.text and (
    get_translation("en", "about") in message.text or
    get_translation("ru", "about") in message.text or
    get_translation("uz", "about") in message.text
))
def about_button(message: telebot.types.Message):
    """Handle about button."""
    # Exit any active modes
    expense_handler.active_expense_mode.discard(message.from_user.id)
    report_handler.active_report_mode.discard(message.from_user.id)
    reminder_handler.active_reminder_mode.discard(message.from_user.id)
    user_states[message.from_user.id] = "none"
    about_handler.handle_about_command(message)


# Expense confirmation callbacks
@bot.callback_query_handler(func=lambda call: call.data == "confirm_yes")
def confirm_expense(call: telebot.types.CallbackQuery):
    """Handle expense confirmation (yes)."""
    expense_handler.handle_expense_confirmation(call, confirmed=True)


@bot.callback_query_handler(func=lambda call: call.data == "confirm_no")
def reject_expense(call: telebot.types.CallbackQuery):
    """Handle expense rejection (no)."""
    expense_handler.handle_expense_confirmation(call, confirmed=False)


# Settings callbacks
@bot.callback_query_handler(func=lambda call: call.data == "settings_lang")
def settings_lang_callback(call: telebot.types.CallbackQuery):
    """Handle language change from settings."""
    settings_handler.handle_language_change(call)


@bot.callback_query_handler(func=lambda call: call.data == "settings_profile")
def settings_profile_callback(call: telebot.types.CallbackQuery):
    """Handle profile edit from settings."""
    settings_handler.handle_profile_edit(call)


@bot.callback_query_handler(func=lambda call: call.data == "settings_timezone")
def settings_timezone_callback(call: telebot.types.CallbackQuery):
    """Handle timezone change from settings."""
    settings_handler.handle_timezone_change(call)


# About callbacks
@bot.callback_query_handler(func=lambda call: call.data == "about_donate")
def about_donate_callback(call: telebot.types.CallbackQuery):
    """Handle donate from about page."""
    about_handler.handle_donate_callback(call)


@bot.callback_query_handler(func=lambda call: call.data == "about_feedback")
def about_feedback_callback(call: telebot.types.CallbackQuery):
    """Handle feedback from about page."""
    about_handler.handle_feedback_callback(call)


# Text message handlers
@bot.message_handler(content_types=['text'])
def text_message_handler(message: telebot.types.Message):
    """Handle text messages."""
    user = db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
    language = user.language or "en"
    
    # Check if user clicked "back" button
    back_texts = [
        get_translation("en", "back"),
        get_translation("ru", "back"),
        get_translation("uz", "back")
    ]
    if message.text in back_texts:
        # Exit all modes
        expense_handler.active_expense_mode.discard(message.from_user.id)
        report_handler.active_report_mode.discard(message.from_user.id)
        reminder_handler.active_reminder_mode.discard(message.from_user.id)
        user_states[message.from_user.id] = "none"
        bot.reply_to(
            message,
            get_translation(language, "main_menu"),
            reply_markup=create_main_keyboard(language)
        )
        return
    
    # Check if waiting for feedback
    if about_handler.handle_feedback_message(message):
        return
    
    # Check if waiting for name update
    if settings_handler.handle_name_update(message):
        return
    
    # Check if user clicked "skip" for timezone
    skip_texts = [
        get_translation("en", "skip"),
        get_translation("ru", "skip"),
        get_translation("uz", "skip")
    ]
    if message.text in skip_texts:
        # User skipped timezone - continue with default flow
        user = db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
        language = user.language or "en"
        
        if language == "en":
            # Show language selection
            bot.reply_to(
                message,
                get_translation("en", "welcome"),
                reply_markup=create_language_keyboard()
            )
        else:
            # Show main menu
            bot.reply_to(
                message,
                get_translation(language, "main_menu"),
                reply_markup=create_main_keyboard(language)
            )
        return
    
    # Check if user has pending expense (waiting for confirmation)
    if message.from_user.id in expense_handler.pending_expenses:
        return
    
    # Check user state and route accordingly
    state = user_states.get(message.from_user.id, "none")
    
    if state == "expense" or expense_handler.is_in_expense_mode(message.from_user.id):
        expense_handler.handle_expense_message(message)
    elif state == "report" or report_handler.is_in_report_mode(message.from_user.id):
        report_handler.handle_report_message(message)
    elif state == "reminder" or reminder_handler.is_in_reminder_mode(message.from_user.id):
        reminder_handler.handle_reminder_message(message)
    else:
        # Default: handle as general chat (reports)
        report_handler.handle_report_message(message)


# Voice message handlers
@bot.message_handler(content_types=['voice'])
def voice_message_handler(message: telebot.types.Message):
    """Handle voice messages."""
    user = db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
    language = user.language or "en"
    
    # Check user state
    state = user_states.get(message.from_user.id, "none")
    
    if state == "expense" or expense_handler.is_in_expense_mode(message.from_user.id):
        expense_handler.handle_expense_voice(message)
    elif state == "reminder" or reminder_handler.is_in_reminder_mode(message.from_user.id):
        reminder_handler.handle_reminder_voice(message)
    else:
        # Default: treat as expense
        expense_handler.handle_expense_voice(message)


# Location message handlers
@bot.message_handler(content_types=['location'])
def location_message_handler(message: telebot.types.Message):
    """Handle location messages to detect timezone."""
    user = db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
    language = user.language or "en"
    
    # Update timezone from location
    from handlers.reminder_handler import get_timezone_from_location
    tz_name = get_timezone_from_location(message.location.latitude, message.location.longitude)
    
    if tz_name:
        try:
            db.update_user_timezone(message.from_user.id, tz_name)
            logger.info(f"Updated timezone for user {user.telegram_id} to {tz_name} from location")
            
            # Check if user was changing timezone from settings
            if message.from_user.id in settings_handler.changing_timezone:
                settings_handler.changing_timezone.discard(message.from_user.id)
                bot.reply_to(
                    message,
                    get_translation(language, "timezone_updated", timezone=tz_name),
                    reply_markup=create_main_keyboard(language)
                )
            # Show appropriate response based on context
            elif user.language == "en" or not user.language:
                # First time user - show language selection
                bot.reply_to(
                    message,
                    get_translation(language, "timezone_updated", timezone=tz_name) + "\n\n" + get_translation("en", "welcome"),
                    reply_markup=create_language_keyboard()
                )
            else:
                # Returning user - show main menu
                bot.reply_to(
                    message,
                    get_translation(language, "timezone_updated", timezone=tz_name),
                    reply_markup=create_main_keyboard(language)
                )
        except Exception as e:
            logger.error(f"Error updating timezone from location: {e}")
            bot.reply_to(message, get_translation(language, "error"))
    else:
        bot.reply_to(message, get_translation(language, "timezone_detection_failed"))


# Error handler
@bot.message_handler(func=lambda message: True)
def default_handler(message: telebot.types.Message):
    """Default handler for unhandled messages."""
    user = db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
    language = user.language or "en"
    
    bot.reply_to(
        message,
        get_translation(language, "error"),
        reply_markup=create_main_keyboard(language)
    )


# Graceful shutdown
def signal_handler(sig, frame):
    """Handle shutdown signals."""
    logger.info("\nShutting down bot...")
    scheduler.shutdown()
    db.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    logger.info("SmartExpenseBot is starting...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except KeyboardInterrupt:
        signal_handler(None, None)

