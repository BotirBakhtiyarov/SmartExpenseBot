"""
Report handler for SmartExpenseBot.
Handles expense report generation using AI.
"""

import telebot
import logging
import re
from datetime import datetime, timedelta
from database import Database
from ai_functions import deepseek_ai_report
from translations import get_translation
from keyboards import create_back_keyboard, create_report_keyboard, create_main_keyboard

logger = logging.getLogger(__name__)


class ReportHandler:
    """Handler for report-related commands."""
    
    def __init__(self, bot: telebot.TeleBot, db: Database):
        self.bot = bot
        self.db = db
        self.active_report_mode = set()  # {user_id} - users in report mode
    
    def handle_report_command(self, message: telebot.types.Message):
        """Handle /reports command or button - show report period buttons."""
        user = self.db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
        language = user.language or "en"
        
        # Show report period selection buttons
        self.bot.reply_to(
            message,
            get_translation(language, "report_prompt"),
            reply_markup=create_report_keyboard(language)
        )
    
    def is_in_report_mode(self, user_id: int) -> bool:
        """Check if user is in report mode."""
        return user_id in self.active_report_mode
    
    def handle_report_message(self, message: telebot.types.Message):
        """Handle report query message (legacy - now uses buttons)."""
        # This is kept for backward compatibility but should not be called
        pass
    
    def generate_report(self, user_id: int, start_date=None, end_date=None, language: str = "en"):
        """Generate and return report for given date range."""
        try:
            # Get user's expenses from database with date filters
            expenses = self.db.get_expenses(user_id, start_date=start_date, end_date=end_date, limit=1000)
            
            if not expenses or len(expenses) == 0:
                no_expenses_msg = {
                    "uz": "Bu davr uchun xarajatlar topilmadi.",
                    "ru": "Расходы за этот период не найдены.",
                    "en": "No expenses found for this period."
                }
                return no_expenses_msg.get(language, "No expenses found for this period.")
            
            # Generate report using AI (DeepSeek_AI_data)
            report_query = f"Show expenses from {start_date.strftime('%Y-%m-%d') if start_date else 'beginning'} to {end_date.strftime('%Y-%m-%d') if end_date else 'now'}"
            report = deepseek_ai_report(report_query, language, expenses)
            
            return self._sanitize_report_text(report)
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return get_translation(language, "error")

    @staticmethod
    def _sanitize_report_text(text: str) -> str:
        """Strip Markdown formatting so Telegram renders plain text."""
        if not text:
            return ""
        
        cleaned = text
        # Remove bold/italic/code markers
        cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
        cleaned = re.sub(r"__(.*?)__", r"\1", cleaned)
        cleaned = re.sub(r"`([^`]*)`", r"\1", cleaned)
        cleaned = cleaned.replace("**", "").replace("__", "")
        # Replace markdown bullet with dash if present
        cleaned = cleaned.replace("* ", "- ")
        return cleaned

