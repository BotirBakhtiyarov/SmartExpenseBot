"""
Expense handler for SmartExpenseBot.
Handles expense input via text and voice messages.
"""

import telebot
from telebot import types
import os
import subprocess
import logging
from database import Database
from ai_functions import deepseek_ai_expense
from translations import get_translation
from keyboards import create_back_keyboard, create_confirm_keyboard
from voice_transcriber import VoiceTranscriber

logger = logging.getLogger(__name__)


class ExpenseHandler:
    """Handler for expense-related commands."""
    
    def __init__(self, bot: telebot.TeleBot, db: Database):
        self.bot = bot
        self.db = db
        self.pending_expenses = {}  # {user_id: expense_data}
        self.active_expense_mode = set()  # {user_id} - users in expense mode
        self.transcriber = VoiceTranscriber()
    
    def handle_expense_command(self, message: telebot.types.Message):
        """Handle /expenses command or button - enter expense mode."""
        user = self.db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
        language = user.language or "en"
        
        # Enter expense mode
        self.active_expense_mode.add(message.from_user.id)
        
        self.bot.reply_to(
            message,
            get_translation(language, "expense_prompt"),
            reply_markup=create_back_keyboard(language)
        )
    
    def is_in_expense_mode(self, user_id: int) -> bool:
        """Check if user is in expense mode."""
        return user_id in self.active_expense_mode
    
    def handle_expense_message(self, message: telebot.types.Message):
        """Handle expense text message."""
        user = self.db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
        language = user.language or "en"
        
        text = message.text.strip()
        
        # Show processing message
        processing_msg = self.bot.reply_to(message, get_translation(language, "processing"))
        
        try:
            # Categorize expense using AI (DeepSeek_AI_1)
            expense_data = deepseek_ai_expense(text, language)
            
            # Store pending expense
            self.pending_expenses[message.from_user.id] = expense_data
            
            # Ask for confirmation with currency
            currency = expense_data.get("currency", "USD")
            confirm_text = get_translation(
                language,
                "expense_confirm",
                amount=expense_data["amount"],
                currency=currency,
                description=expense_data["description"],
                category=expense_data["category"]
            )
            
            # Edit message with confirmation
            self.bot.edit_message_text(
                confirm_text,
                chat_id=message.chat.id,
                message_id=processing_msg.message_id,
                reply_markup=create_confirm_keyboard(language)
            )
        except Exception as e:
            logger.error(f"Error processing expense message: {e}")
            self.bot.edit_message_text(
                get_translation(language, "error"),
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
    
    def handle_expense_voice(self, message: telebot.types.Message):
        """Handle expense voice message."""
        user = self.db.get_or_create_user(message.from_user.id, message.from_user.first_name or "User")
        language = user.language or "en"
        
        # Download voice file
        file_info = self.bot.get_file(message.voice.file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)
        
        # Save to temporary file
        temp_path = f"/tmp/voice_{message.from_user.id}.ogg"
        with open(temp_path, "wb") as f:
            f.write(downloaded_file)
        
        # Show processing message
        processing_msg = self.bot.reply_to(message, get_translation(language, "processing"))
        
        try:
            # Transcribe voice
            transcribed_text = self.transcriber.transcribe(temp_path, language)
            
            if not transcribed_text or "not available" in transcribed_text.lower():
                self.bot.edit_message_text(
                    transcribed_text or get_translation(language, "error"),
                    chat_id=message.chat.id,
                    message_id=processing_msg.message_id
                )
                return
            
            # Categorize expense using AI
            expense_data = deepseek_ai_expense(transcribed_text, language)
            
            # Store pending expense
            self.pending_expenses[message.from_user.id] = expense_data
            
            # Ask for confirmation with currency
            currency = expense_data.get("currency", "USD")
            confirm_text = get_translation(
                language,
                "expense_confirm",
                amount=expense_data["amount"],
                currency=currency,
                description=expense_data["description"],
                category=expense_data["category"]
            )
            
            # Edit message with confirmation
            self.bot.edit_message_text(
                confirm_text,
                chat_id=message.chat.id,
                message_id=processing_msg.message_id,
                reply_markup=create_confirm_keyboard(language)
            )
        
        except Exception as e:
            logger.error(f"Error processing expense voice: {e}")
            self.bot.edit_message_text(
                get_translation(language, "error"),
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def handle_expense_confirmation(self, call: telebot.types.CallbackQuery, confirmed: bool):
        """Handle expense confirmation (yes/no)."""
        user = self.db.get_or_create_user(call.from_user.id, call.from_user.first_name or "User")
        language = user.language or "en"
        
        if call.from_user.id not in self.pending_expenses:
            self.bot.answer_callback_query(call.id, get_translation(language, "error"))
            return
        
        self.bot.answer_callback_query(call.id)
        
        if confirmed:
            expense_data = self.pending_expenses[call.from_user.id]
            
            # Save to database
            self.db.add_expense(
                call.from_user.id,
                expense_data["amount"],
                expense_data["category"],
                expense_data["description"]
            )
            
            # Send confirmation
            response = get_translation(language, "expense_confirmed")
            if expense_data.get("advice"):
                response += f"\n\n{expense_data['advice']}"
            
            self.bot.edit_message_text(
                response,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            
            # Remove pending expense
            del self.pending_expenses[call.from_user.id]
        else:
            # User rejected
            del self.pending_expenses[call.from_user.id]
            self.bot.edit_message_text(
                get_translation(language, "expense_prompt"),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )

