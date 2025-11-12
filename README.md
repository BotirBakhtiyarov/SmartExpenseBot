# SmartExpenseBot

<div align="center">

**A smart personal assistant Telegram bot for expense tracking, spending reports, and reminders**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## 🎯 Overview

SmartExpenseBot is an intelligent Telegram bot that helps users manage their personal finances through natural language interactions. Powered by **DeepSeek AI** and built with **pyTelegramBotAPI**, it provides seamless expense tracking, detailed spending reports, and smart reminder functionality.

### Key Capabilities

- **AI-Powered Expense Tracking**: Automatically categorize expenses from natural language input
- **Intelligent Reporting**: Generate comprehensive spending reports using conversational queries
- **Smart Reminders**: Set and manage reminders with automatic notifications
- **Multi-language Support**: Available in English, Russian, and Uzbek
- **Voice Integration**: Support for voice message transcription and processing

## ✨ Features

### 💸 Expense Management
- Track expenses via text or voice messages
- AI-powered automatic categorization
- Support for multiple currencies
- Confirmation workflow for accuracy

### 📊 Advanced Reporting
- Natural language query interface
- Time-based filtering (daily, weekly, monthly)
- Category-based analysis
- Visual expense summaries

### ⏰ Reminder System
- Set reminders using natural language
- Dual notification system (10 minutes before + exact time)
- Timezone-aware scheduling
- Automatic timezone detection from location

### 🌍 Internationalization
- Full support for English, Russian, and Uzbek
- Language-specific date/time parsing
- Localized user interface

### 🎤 Voice Support
- Voice message transcription using Vosk
- Multi-language speech recognition
- Seamless integration with expense and reminder features

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **Bot Framework** | pyTelegramBotAPI 4.14.0 |
| **Database** | SQLAlchemy (SQLite3 / PostgreSQL) |
| **AI Integration** | DeepSeek API |
| **Speech Recognition** | Vosk 0.3.45 |
| **Task Scheduling** | APScheduler 3.10.4 |
| **Audio Processing** | FFmpeg, pydub |
| **Timezone Handling** | pytz, timezonefinderL |

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **FFmpeg** (for audio processing)
- **Telegram Bot Token** (obtain from [@BotFather](https://t.me/BotFather))
- **DeepSeek API Key** (obtain from [DeepSeek Platform](https://platform.deepseek.com/))
- **Vosk Models** (optional, for voice transcription)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/botirbakhtiyarov/SmartExpenseBot.git
cd SmartExpenseBot
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download and install from [FFmpeg Official Website](https://ffmpeg.org/download.html)

### Step 5: Download Vosk Models (Optional)

For voice transcription support, download language models from [Vosk Models](https://alphacephei.com/vosk/models):

- `vosk-model-small-uz-0.22` (Uzbek)
- `vosk-model-small-ru-0.22` (Russian)
- `vosk-model-small-en-us-0.22` (English)

Extract each model to the corresponding directory:
```
./models/vosk-model-uz/
./models/vosk-model-ru/
./models/vosk-model-en/
```

## ⚙️ Configuration

### Step 1: Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### Step 2: Configure Environment Variables

Edit `.env` and provide your credentials:

```env
# Required: Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here

# Required: DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

# Optional: Developer Configuration
DEVELOPER_ID=your_telegram_user_id

# Database Configuration
DB_TYPE=sqlite
SQLITE_DB_PATH=smart_expense_bot.db

# Optional: Proxy Configuration
# PROXY_URL=socks5://127.0.0.1:10808
```

### Step 3: Verify Configuration

Run the bot to verify your configuration:

```bash
python bot.py
```

## 📖 Usage

### Starting the Bot

```bash
python bot.py
```

The bot will start polling for messages. You should see a confirmation message in the logs.

### Basic Commands

#### Adding Expenses

1. Click the **"💸 Expenses"** button in the main menu
2. Send your expense via text or voice:
   - Text: `"I spent 50 yuan on lunch"`
   - Voice: Record a voice message describing your expense
3. Review the AI-categorized expense
4. Confirm to save

#### Generating Reports

1. Click the **"📊 Reports"** button
2. Ask questions in natural language:
   - `"Show my food expenses this month"`
   - `"What did I spend on transportation last week?"`
   - `"Total expenses in December"`
3. Receive detailed spending analysis

#### Setting Reminders

1. Click the **"⏰ Reminders"** button
2. Create reminders using natural language:
   - `"Remind me to pay bills tomorrow at 3 PM"`
   - `"Remind me in 2 hours to call mom"`
3. Receive notifications 10 minutes before and at the scheduled time

#### Managing Settings

1. Click the **"⚙️ Settings"** button
2. Change language preference
3. Update profile information
4. Configure timezone (automatic detection available)

## 📁 Project Structure

```
SmartExpenseBot/
│
├── handlers/                      # Bot command handlers
│   ├── __init__.py
│   ├── expense_handler.py         # Expense tracking logic
│   ├── report_handler.py          # Report generation logic
│   ├── reminder_handler.py        # Reminder management logic
│   ├── settings_handler.py        # Settings and profile management
│   └── about_handler.py           # About page and feedback
│
├── ai_functions.py                # DeepSeek AI integration
│                                   # (3 specialized AI instances)
├── bot.py                         # Main bot application
├── config.py                      # Configuration management
├── database.py                    # Database models and utilities
├── keyboards.py                   # Keyboard creation utilities
├── translations.py                # Multi-language translations
├── voice_transcriber.py           # Voice transcription (Vosk)
├── scheduler.py                   # Reminder scheduler (APScheduler)
│
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── LICENSE                        # MIT License
└── README.md                      # This file
```

## 🔌 API Reference

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | ✅ Yes | - |
| `DEEPSEEK_API_KEY` | DeepSeek API key | ✅ Yes | - |
| `DEEPSEEK_API_URL` | DeepSeek API endpoint | ✅ Yes | `https://api.deepseek.com/v1/chat/completions` |
| `DEVELOPER_ID` | Telegram user ID for feedback | ❌ No | `0` |
| `DB_TYPE` | Database type: `sqlite` or `postgresql` | ✅ Yes | `sqlite` |
| `SQLITE_DB_PATH` | SQLite database file path | If SQLite | `smart_expense_bot.db` |
| `POSTGRES_HOST` | PostgreSQL host address | If PostgreSQL | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | If PostgreSQL | `5432` |
| `POSTGRES_DB` | PostgreSQL database name | If PostgreSQL | `smart_expense_bot` |
| `POSTGRES_USER` | PostgreSQL username | If PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | If PostgreSQL | `postgres` |
| `PROXY_URL` | Proxy URL (optional) | ❌ No | - |
| `VOSK_MODEL_PATH_UZ` | Path to Uzbek Vosk model | ❌ No | `./models/vosk-model-uz` |
| `VOSK_MODEL_PATH_RU` | Path to Russian Vosk model | ❌ No | `./models/vosk-model-ru` |
| `VOSK_MODEL_PATH_EN` | Path to English Vosk model | ❌ No | `./models/vosk-model-en` |

### AI Functions

The bot utilizes three specialized DeepSeek AI instances:

1. **DeepSeek_AI_1**: Expense extraction and categorization
   - Extracts amount, category, and description from natural language
   - Provides intelligent expense categorization

2. **DeepSeek_AI_2**: Reminder time parsing
   - Parses natural language time expressions
   - Handles relative and absolute time references
   - Timezone-aware parsing

3. **DeepSeek_AI_data**: Report generation and analysis
   - Generates comprehensive spending reports
   - Analyzes expense patterns
   - Provides insights and summaries

## 🔧 Troubleshooting

### Bot Not Responding

**Symptoms**: Bot doesn't respond to messages

**Solutions**:
- Verify `BOT_TOKEN` is correct and active
- Check bot is running (review application logs)
- Ensure bot has necessary permissions in Telegram
- Verify network connectivity

### Database Errors

**Symptoms**: Database connection or query errors

**Solutions**:
- Verify database credentials are correct
- For PostgreSQL, check connection string format
- Ensure database tables are created (auto-created on first run)
- Check database server is running and accessible
- Review database logs for detailed error messages

### Concurrent User Issues

**Symptoms**: Errors when multiple users use the bot simultaneously

**Solutions**:
- The bot uses thread-safe database sessions (scoped sessions) to handle concurrent requests
- Each user request gets its own isolated database session
- If you experience issues, ensure you're using the latest version with thread-safe session management
- For SQLite, the bot is configured with `check_same_thread=False` and connection pooling
- For PostgreSQL, connection pooling is enabled by default

### Voice Transcription Not Working

**Symptoms**: Voice messages are not transcribed

**Solutions**:
- Verify Vosk models are downloaded and in correct paths
- Check model paths in environment variables
- Ensure FFmpeg is installed and accessible
- Verify audio format is supported (OGG, MP3, WAV)
- Check available disk space for temporary files

### AI Categorization Not Working

**Symptoms**: Expenses are not being categorized correctly

**Solutions**:
- Verify `DEEPSEEK_API_KEY` is valid and active
- Check API endpoint URL is correct
- Review API rate limits and quotas
- Check network connectivity to DeepSeek API
- Review API response logs for errors

### Timezone Detection Issues

**Symptoms**: Reminders scheduled at wrong times

**Solutions**:
- Ensure user has shared location for timezone detection
- Verify timezonefinderL is installed: `pip install timezonefinderL`
- Check timezone API connectivity
- Manually set timezone in settings if automatic detection fails

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation as needed
- Test your changes thoroughly
- Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 👤 Author

**Botir Bakhtiyarov**

- GitHub: [@botirbakhtiyarov](https://github.com/botirbakhtiyarov)
- Telegram: [@bakhtiyarovbotir](https://t.me/bakhtiyarovbotir)

## 🙏 Acknowledgments

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - Telegram Bot API wrapper
- [DeepSeek](https://www.deepseek.com/) - AI API provider
- [Vosk](https://alphacephei.com/vosk/) - Speech recognition engine
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit
- [APScheduler](https://apscheduler.readthedocs.io/) - Task scheduling library

## 📞 Support

For issues, questions, or feature requests:

- **GitHub Issues**: [Open an issue](https://github.com/botirbakhtiyarov/SmartExpenseBot/issues)
- **Telegram**: Use the bot's "About Us" → "Feedback" feature
- **Email**: [botirbakhtiyarovb@gmail.com](mailto:botirbakhtiyarovb@gmail.com)

---

<div align="center">

**Made with ❤️ by Botir Bakhtiyarov**

⭐ Star this repo if you find it helpful!

</div>
