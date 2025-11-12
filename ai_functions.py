"""
DeepSeek API integration for SmartExpenseBot.
Three specialized AI functions for different tasks.
"""

import requests
import json
import logging
from typing import Dict, Optional
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)


def deepseek_ai_expense(text: str, lang: str = "en") -> Dict:
    """
    DeepSeek_AI_1: Specialized for expense extraction and categorization.
    
    Args:
        text: User's expense description
        lang: User's language preference (uz, ru, en)
    
    Returns:
        Dictionary with amount, category, description, currency, and advice
    """
    prompts = {
        "uz": f"""Quyidagi xarajatni tahlil qiling va quyidagi formatda JSON javob bering:
{{
    "amount": <raqam>,
    "currency": "<valyuta>",
    "category": "<kategoriya>",
    "description": "<tavsif>",
    "advice": "<tavsiya yoki bo'sh string>"
}}

MUHIM: Valyutani matndan aniqlang (masalan: USD, EUR, CNY, RMB, Yuan, Dollar, Euro, so'm, rubl, va hokazo). Agar valyuta ko'rsatilmagan bo'lsa, "USD" dan foydalaning.

Kategoriyalar: Food, Transport, Entertainment, Education, Health, Electronics, Shopping, Bills, Other
Xarajat: {text}""",
        "ru": f"""Проанализируйте следующий расход и верните JSON ответ в следующем формате:
{{
    "amount": <число>,
    "currency": "<валюта>",
    "category": "<категория>",
    "description": "<описание>",
    "advice": "<совет или пустая строка>"
}}

ВАЖНО: Определите валюту из текста (например: USD, EUR, CNY, RMB, Yuan, Dollar, Euro, доллар, юань, рубль и т.д.). Если валюта не указана, используйте "USD".

Категории: Food, Transport, Entertainment, Education, Health, Electronics, Shopping, Bills, Other
Расход: {text}""",
        "en": f"""Analyze the following expense and return a JSON response in the following format:
{{
    "amount": <number>,
    "currency": "<currency>",
    "category": "<category>",
    "description": "<description>",
    "advice": "<advice or empty string>"
}}

IMPORTANT: Detect the currency from the text (e.g., USD, EUR, CNY, RMB, Yuan, Dollar, Euro, dollars, yuan, etc.). If no currency is mentioned, use "USD".

Categories: Food, Transport, Entertainment, Education, Health, Electronics, Shopping, Bills, Other
Expense: {text}"""
    }
    
    prompt = prompts.get(lang, prompts["en"])
    
    try:
        headers = {
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are DeepSeek_AI_1 - specialized for expense extraction and categorization. CRITICAL: Each request is completely independent - do NOT use any context from previous requests. Your ONLY job is to extract expense information (amount, currency, category, description) from the CURRENT user message and return valid JSON. You MUST detect the currency from the text itself (USD, EUR, CNY, RMB, Yuan, Dollar, Euro, etc.). If no currency is mentioned, default to USD. You do NOT add expenses to database - you only extract information for confirmation."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        
        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Try to extract JSON from response
            try:
                # Remove markdown code blocks if present
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                result = json.loads(content)
                
                # Validate and set defaults
                amount_value = result.get("amount")
                if amount_value is None:
                    amount = 0.0
                else:
                    try:
                        amount = float(amount_value)
                    except (ValueError, TypeError):
                        amount = 0.0
                
                # Extract currency - normalize common variations
                currency_raw = result.get("currency", "USD").upper().strip()
                currency_map = {
                    "YUAN": "CNY", "RMB": "CNY", "CN¥": "CNY", "¥": "CNY",
                    "DOLLAR": "USD", "DOLLARS": "USD", "$": "USD", "US$": "USD",
                    "EURO": "EUR", "EUROS": "EUR", "€": "EUR",
                    "RUBLE": "RUB", "RUBLES": "RUB", "RUBL": "RUB", "₽": "RUB",
                    "SOM": "UZS", "SO'M": "UZS", "UZS": "UZS"
                }
                currency = currency_map.get(currency_raw, currency_raw if len(currency_raw) <= 5 else "USD")
                
                category = result.get("category", "Other")
                description = result.get("description", text)
                advice = result.get("advice", "")
                
                return {
                    "amount": amount,
                    "currency": currency,
                    "category": category,
                    "description": description,
                    "advice": advice
                }
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error in expense AI: {e}")
                return _extract_expense_manually(text, lang)
        else:
            logger.error(f"DeepSeek API error in expense AI: {response.status_code}")
            return _extract_expense_manually(text, lang)
    
    except Exception as e:
        logger.error(f"Error calling DeepSeek API for expense: {e}")
        return _extract_expense_manually(text, lang)


def deepseek_ai_report(text: str, lang: str = "en", expenses_data: list = None) -> str:
    """
    DeepSeek_AI_data: Generate expense reports based on user queries.
    
    Args:
        text: User's report query
        lang: User's language preference
        expenses_data: List of expense objects from database
    
    Returns:
        Formatted report string
    """
    # Prepare context with expenses
    expenses_context = ""
    if expenses_data:
        total = sum(e.amount for e in expenses_data)
        categories = {}
        for e in expenses_data:
            cat = e.category or "Other"
            categories[cat] = categories.get(cat, 0) + e.amount
        
        expenses_context = f"\n\nUser's expenses (total {len(expenses_data)} records):\n"
        expenses_context += f"Total amount: {total:.2f}\n"
        expenses_context += "By category:\n"
        for cat, amount in categories.items():
            expenses_context += f"- {cat}: {amount:.2f}\n"
        expenses_context += "\nRecent expense details:\n"
        for e in expenses_data[:15]:
            date_str = e.date.strftime("%Y-%m-%d") if e.date else 'N/A'
            expenses_context += f"- {date_str}: {e.amount:.2f} ({e.category}): {e.description or ''}\n"
    else:
        expenses_context = "\n\nUser has no expenses recorded yet."
    
    prompts = {
        "uz": f"""Siz foydalanuvchining shaxsiy yordamchisisiz va uning ma'lumotlar bazasiga ulangansiz.
Sizning vazifangiz: foydalanuvchi bilan uning xarajatlari haqida suhbatlashish, hisobotlar berish, savollarga javob berish.

MUHIM: 
- Siz xarajatlar qo'sha OLMAYSIZ - faqat o'qish va hisobot berish mumkin
- Agar foydalanuvchi xarajat qo'shmoqchi bo'lsa, "Xarajatlar" tugmasini bosishi kerak
- Siz faqat mavjud ma'lumotlar haqida gapirasiz va hisobot berasiz

Foydalanuvchi so'rovi: {text}
{expenses_context}

Javob bering va kerak bo'lsa, ma'lumotlar bazasidagi ma'lumotlardan foydalaning.""",
        "ru": f"""Вы личный помощник пользователя, подключенный к его базе данных.
Ваша задача: общаться с пользователем о его расходах, предоставлять отчеты, отвечать на вопросы.

ВАЖНО:
- Вы НЕ МОЖЕТЕ добавлять расходы - только читать и предоставлять отчеты
- Если пользователь хочет добавить расход, он должен нажать кнопку "Расходы"
- Вы только обсуждаете существующие данные и предоставляете отчеты

Запрос пользователя: {text}
{expenses_context}

Ответьте и при необходимости используйте данные из базы данных.""",
        "en": f"""You are the user's personal assistant, connected to their database.
Your task: chat with the user about their expenses, provide reports, answer questions.

IMPORTANT:
- You CANNOT add expenses - you can only read and provide reports
- If the user wants to add an expense, they must press the "Expenses" button
- You only discuss existing data and provide reports

User's query: {text}
{expenses_context}

Respond and use database information if relevant."""
    }
    
    prompt = prompts.get(lang, prompts["en"])
    
    try:
        headers = {
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are DeepSeek_AI_data - a personal assistant connected to the user's database. You can ONLY read and discuss existing records (expenses). You CANNOT add, modify, or delete any records. If the user wants to add records, direct them to use the appropriate function buttons. Your role is to provide reports, answer questions, and give advice based on existing data."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content.strip()
        else:
            logger.error(f"DeepSeek API error in report AI: {response.status_code}")
            return "Error generating report. Please try again."
    
    except Exception as e:
        logger.error(f"Error calling DeepSeek API for report: {e}")
        return "Error generating report. Please try again."


def deepseek_ai_reminder(text: str, lang: str = "en", user_timezone: str = "UTC", current_time: datetime = None) -> Optional[str]:
    """
    DeepSeek_AI_2: Specialized for reminder time extraction.
    
    Args:
        text: User's reminder text with time
        lang: User's language preference
        user_timezone: User's timezone (e.g., 'Asia/Tashkent', 'Europe/Moscow')
        current_time: Current datetime in user's timezone (datetime object)
    
    Returns:
        ISO format datetime string or None
    """
    prompts = {
        "uz": f"""Quyidagi matndan vaqtni ajratib oling va ISO formatda qaytaring (YYYY-MM-DD HH:MM:SS):
Matn: {text}
Agar vaqt topilmasa, None qaytaring.""",
        "ru": f"""Извлеките время из следующего текста и верните в формате ISO (YYYY-MM-DD HH:MM:SS):
Текст: {text}
Если время не найдено, верните None.""",
        "en": f"""Extract time from the following text and return in ISO format (YYYY-MM-DD HH:MM:SS):
Text: {text}
If time is not found, return None."""
    }
    
    prompt = prompts.get(lang, prompts["en"])
    
    try:
        headers = {
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Get current time in user's timezone for context
        if current_time:
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            current_time_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"You are DeepSeek_AI_2 - specialized for reminder time extraction. Your ONLY job is to extract time/date information from user messages and return ISO format datetime string (YYYY-MM-DD HH:MM:SS). IMPORTANT: The user is in timezone {user_timezone}. Current local time: {current_time_str}. For relative times like 'after 15 minutes', 'in 30 minutes', calculate the actual future datetime from the current local time. Return only the ISO datetime string or 'None' if time cannot be extracted."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        
        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            
            if content.lower() == "none" or not content:
                return None
            
            return content
        else:
            logger.error(f"DeepSeek API error in reminder AI: {response.status_code}")
            return None
    
    except Exception as e:
        logger.error(f"Error calling DeepSeek API for reminder: {e}")
        return None


def _extract_expense_manually(text: str, lang: str) -> Dict:
    """Fallback manual extraction if API fails."""
    import re
    
    # Try to extract numbers
    numbers = re.findall(r'\d+\.?\d*', text)
    amount = float(numbers[0]) if numbers else 0.0
    
    # Simple keyword-based categorization
    text_lower = text.lower()
    category = "Other"
    
    food_keywords = ["burger", "food", "restaurant", "eat", "meal", "pizza", "osh", "non", "taom", "еда", "ресторан", "lunch", "dinner", "breakfast"]
    transport_keywords = ["taxi", "bus", "train", "transport", "taksi", "avtobus", "mashina", "такси", "автобус"]
    entertainment_keywords = ["cinema", "movie", "game", "entertainment", "kino", "o'yin", "кино", "игра"]
    education_keywords = ["book", "course", "education", "kitob", "kurs", "ta'lim", "книга", "курс"]
    health_keywords = ["doctor", "medicine", "hospital", "health", "doktor", "dori", "shifoxona", "доктор", "лекарство"]
    electronics_keywords = ["phone", "computer", "electronic", "telefon", "kompyuter", "телефон", "компьютер"]
    
    if any(kw in text_lower for kw in food_keywords):
        category = "Food"
    elif any(kw in text_lower for kw in transport_keywords):
        category = "Transport"
    elif any(kw in text_lower for kw in entertainment_keywords):
        category = "Entertainment"
    elif any(kw in text_lower for kw in education_keywords):
        category = "Education"
    elif any(kw in text_lower for kw in health_keywords):
        category = "Health"
    elif any(kw in text_lower for kw in electronics_keywords):
        category = "Electronics"
    
    # Try to detect currency from text
    currency = "USD"  # Default
    if any(word in text_lower for word in ["yuan", "rmb", "cny", "¥"]):
        currency = "CNY"
    elif any(word in text_lower for word in ["dollar", "usd", "$"]):
        currency = "USD"
    elif any(word in text_lower for word in ["euro", "eur", "€"]):
        currency = "EUR"
    elif any(word in text_lower for word in ["ruble", "rub", "₽"]):
        currency = "RUB"
    elif any(word in text_lower for word in ["som", "so'm", "uzs"]):
        currency = "UZS"
    
    return {
        "amount": amount,
        "currency": currency,
        "category": category,
        "description": text,
        "advice": ""
    }

