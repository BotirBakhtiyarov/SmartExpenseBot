"""
Configuration management for SmartExpenseBot.
Loads environment variables and provides configuration access.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot configuration class."""
    
    # Telegram Bot
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    DEVELOPER_ID = int(os.getenv("DEVELOPER_ID", "0"))
    
    # DeepSeek API
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    
    # Database
    DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "smart_expense_bot.db")
    
    # PostgreSQL (if DB_TYPE is postgresql)
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "smart_expense_bot")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    
    # Vosk Models
    VOSK_MODEL_PATH_UZ = os.getenv("VOSK_MODEL_PATH_UZ", "./models/vosk-model-uz")
    VOSK_MODEL_PATH_RU = os.getenv("VOSK_MODEL_PATH_RU", "./models/vosk-model-ru")
    VOSK_MODEL_PATH_EN = os.getenv("VOSK_MODEL_PATH_EN", "./models/vosk-model-en")
    
    # Proxy (optional)
    PROXY_URL = os.getenv("PROXY_URL", "")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required in .env file")
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY is required in .env file")
        return True

