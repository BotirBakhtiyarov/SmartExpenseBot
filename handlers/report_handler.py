"""
Report handler for SmartExpenseBot.
Handles expense report generation using AI.
"""

import telebot
import logging
from database import Database
from ai_functions import deepseek_ai_report
from translations import get_translation
from keyboards import create_back_keyboard

logger = logging.getLogger(__name__)


class ReportHandler:
    """Handler for report-related commands."""
    
    def __init__(self, bot: telebot.TeleBot, db: Database):
        self.bot = bot
        self.db = db
        self.active_report_mode = set()  # {user_id} - users in report mode
    
    def handle_report_command(self, message: telebot.types.Message):
        """Handle /reports command or button - enter report mode."""
        user = self.db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
        language = user.language or "en"
        
        # Enter report mode
        self.active_report_mode.add(message.from_user.id)
        
        self.bot.reply_to(
            message,
            get_translation(language, "report_prompt"),
            reply_markup=create_back_keyboard(language)
        )
    
    def is_in_report_mode(self, user_id: int) -> bool:
        """Check if user is in report mode."""
        return user_id in self.active_report_mode
    
    def handle_report_message(self, message: telebot.types.Message):
        """Handle report query message."""
        user = self.db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
        language = user.language or "en"
        
        text = message.text.strip()
        
        # Show processing message
        processing_msg = self.bot.reply_to(message, get_translation(language, "processing"))
        
        try:
            # Get user's expenses from database
            expenses = self.db.get_expenses(message.from_user.id, limit=100)
            
            # Generate report using AI (DeepSeek_AI_data)
            report = deepseek_ai_report(text, language, expenses)
            
            # Edit message with report
            self.bot.edit_message_text(
                report,
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            self.bot.edit_message_text(
                get_translation(language, "error"),
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )

