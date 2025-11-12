"""
Translation system for multilingual support.
Supports Uzbek, Russian, and English.
"""

TRANSLATIONS = {
    "uz": {
        "welcome": "Assalomu alaykum! Men SmartExpenseBot - sizning shaxsiy yordamchingizman. Tilni tanlang:",
        "language_set": "Til o'zgartirildi: O'zbek tili",
        "main_menu": "Asosiy menyu",
        "expenses": "💸 Xarajatlar",
        "reports": "📊 Hisobotlar",
        "reminders": "⏰ Eslatmalar",
        "settings": "⚙️ Sozlamalar",
        "about": "ℹ️ Biz haqimizda",
        "back": "⬅️ Orqaga",
        "expense_prompt": "Xarajatni matn yoki ovozli xabar orqali yuboring:",
        "expense_confirmed": "Xarajat saqlandi! 💰",
        "expense_confirm": "Siz {amount} {currency} {description} uchun sarfladingiz (Kategoriya: {category}). Saqlashni tasdiqlaysizmi?",
        "yes": "Ha",
        "no": "Yo'q",
        "report_prompt": "Hisobot so'rovingizni yuboring (masalan: 'Bu oygi xarajatlarimni ko'rsating'):",
        "reminder_prompt": "Eslatmani matn yoki ovozli xabar orqali yuboring:",
        "reminder_added": "Eslatma qo'shildi! ⏰",
        "request_location_for_timezone": "Vaqt mintaqasini aniqlash uchun joylashuvingizni yuboring:",
        "share_location": "📍 Joylashuvni yuborish",
        "skip": "O'tkazib yuborish",
        "reminder_warning": "⏰ Eslatma (10 daqiqa qoldi):\n{message}",
        "reminder_triggered": "🔔 Eslatma:\n{message}",
        "settings_menu": "Sozlamalar",
        "change_language": "Tilni o'zgartirish",
        "edit_profile": "Profilni tahrirlash",
        "change_timezone": "Vaqt mintaqasini o'zgartirish",
        "user_info": "Ism: {name}\nTil: {lang_name}\nVaqt mintaqasi: {timezone}",
        "feedback_prompt": "Fikr-mulohazangizni yuboring:",
        "feedback_sent": "Fikr-mulohazangiz yuborildi! Rahmat! 🙏",
        "error": "Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
        "processing": "Qayta ishlanmoqda...",
        "timezone_updated": "Vaqt mintaqasi yangilandi: {timezone}",
        "timezone_detection_failed": "Vaqt mintaqasini aniqlashda xatolik yuz berdi.",
        "about_text": "SmartExpenseBot — sizning kundalik xarajatlaringizni boshqarish, hisobotlar olish va eslatmalarni avtomatik tarzda olishda yordam beruvchi aqlli yordamchingizdir.\nBu bot orqali siz o‘z moliyaviy holatingizni nazorat qilib, har bir sarfingizni tahlil qila olasiz.\n\nBiz ushbu loyihani foydalanuvchilarga qulay, tejamkor va aqlli moliyaviy boshqaruv imkoniyatini berish maqsadida yaratdik.\n\nAgar sizga SmartExpenseBot yoqsa va bizni qo‘llab-quvvatlamoqchi bo‘lsangiz, biz uchun bu juda katta ilhom bo‘ladi.\n💬 Fikr-mulohazalaringizni yozib qoldiring va ❤️ istasangiz, kichik donat orqali loyihani rivojlantirishimizga yordam bering.\n\nMuallif: Botir Bakhtiyarov 🇺🇿",
    },
    "ru": {
        "welcome": "Здравствуйте! Я SmartExpenseBot - ваш личный помощник. Выберите язык:",
        "language_set": "Язык изменен: Русский",
        "main_menu": "Главное меню",
        "expenses": "💸 Расходы",
        "reports": "📊 Отчеты",
        "reminders": "⏰ Напоминания",
        "settings": "⚙️ Настройки",
        "about": "ℹ️ О нас",
        "back": "⬅️ Назад",
        "expense_prompt": "Отправьте расход текстом или голосовым сообщением:",
        "expense_confirmed": "Расход сохранен! 💰",
        "expense_confirm": "Вы потратили {amount} {currency} на {description} (Категория: {category}). Подтвердить сохранение?",
        "yes": "Да",
        "no": "Нет",
        "report_prompt": "Отправьте запрос отчета (например: 'Покажи мои расходы за этот месяц'):",
        "reminder_prompt": "Отправьте напоминание текстом или голосовым сообщением:",
        "reminder_added": "Напоминание добавлено! ⏰",
        "request_location_for_timezone": "Поделитесь местоположением для определения часового пояса:",
        "share_location": "📍 Поделиться местоположением",
        "skip": "Пропустить",
        "reminder_warning": "⏰ Напоминание (осталось 10 минут):\n{message}",
        "reminder_triggered": "🔔 Напоминание:\n{message}",
        "settings_menu": "Настройки",
        "change_language": "Изменить язык",
        "edit_profile": "Редактировать профиль",
        "change_timezone": "Изменить часовой пояс",
        "user_info": "Имя: {name}\nЯзык: {lang_name}\nЧасовой пояс: {timezone}",
        "feedback_prompt": "Отправьте ваш отзыв:",
        "feedback_sent": "Ваш отзыв отправлен! Спасибо! 🙏",
        "error": "Произошла ошибка. Пожалуйста, попробуйте еще раз.",
        "processing": "Обработка...",
        "timezone_updated": "Часовой пояс обновлен: {timezone}",
        "timezone_detection_failed": "Не удалось определить часовой пояс.",
        "about_text": "SmartExpenseBot — ваш интеллектуальный помощник для управления ежедневными расходами, генерации отчетов и получения полезных напоминаний.\nС этим ботом вы можете легко отслеживать свои финансы и анализировать, куда ваши деньги идут.\nМы создали этот проект, чтобы сделать управление финансами простым, умным и доступным для всех.\n\nЕсли вам нравится использовать SmartExpenseBot и вы хотите поддержать нашу работу, ваши отзывы и пожертвования значимы для нас.\n💬 Поделитесь своими мыслями и ❤️ поддержите нас маленьким пожертвованием, чтобы помочь нам развивать и улучшать этот проект.\n\nМужчина: Botir Bakhtiyarov 🇺🇿",
    },
    "en": {
        "welcome": "Hello! I'm SmartExpenseBot - your personal assistant. Choose a language:",
        "language_set": "Language changed: English",
        "main_menu": "Main Menu",
        "expenses": "💸 Expenses",
        "reports": "📊 Reports",
        "reminders": "⏰ Reminders",
        "settings": "⚙️ Settings",
        "about": "ℹ️ About Us",
        "back": "⬅️ Back",
        "expense_prompt": "Send an expense via text or voice message:",
        "expense_confirmed": "Expense saved! 💰",
        "expense_confirm": "You spent {amount} {currency} on {description} (Category: {category}). Confirm to save?",
        "yes": "Yes",
        "no": "No",
        "report_prompt": "Send your report query (e.g., 'Show my expenses this month'):",
        "reminder_prompt": "Send a reminder via text or voice message:",
        "reminder_added": "Reminder added! ⏰",
        "request_location_for_timezone": "Please share your location to detect your timezone:",
        "share_location": "📍 Share Location",
        "skip": "Skip",
        "reminder_warning": "⏰ Reminder (10 minutes left):\n{message}",
        "reminder_triggered": "🔔 Reminder:\n{message}",
        "settings_menu": "Settings",
        "change_language": "Change Language",
        "edit_profile": "Edit Profile",
        "change_timezone": "Change Timezone",
        "user_info": "Name: {name}\nLanguage: {lang_name}\nTimezone: {timezone}",
        "feedback_prompt": "Send your feedback:",
        "feedback_sent": "Your feedback has been sent! Thank you! 🙏",
        "error": "An error occurred. Please try again.",
        "processing": "Processing...",
        "timezone_updated": "Timezone updated: {timezone}",
        "timezone_detection_failed": "Failed to detect timezone.",
        "about_text": "SmartExpenseBot is your intelligent assistant for managing daily expenses, generating reports, and receiving helpful reminders.\nWith this bot, you can easily keep track of your finances and analyze where your money goes.\nWe built this project to make financial management simple, smart, and accessible for everyone.\n\nIf you enjoy using SmartExpenseBot and want to support our work, your feedback and donations mean the world to us.\n💬 Share your thoughts and ❤️ support us with a small donation to help us grow and improve this project.\n\nCreated by: Botir Bakhtiyarov 🇺🇿",
    }
}


def get_translation(language: str, key: str, **kwargs) -> str:
    """
    Get translation for a given language and key.
    
    Args:
        language: Language code (uz, ru, en)
        key: Translation key
        **kwargs: Format arguments for the translation string
    
    Returns:
        Translated string
    """
    lang = language if language in TRANSLATIONS else "en"
    translation = TRANSLATIONS[lang].get(key, key)
    
    if kwargs:
        try:
            return translation.format(**kwargs)
        except KeyError:
            return translation
    
    return translation


def get_language_name(code: str) -> str:
    """Get language name from code."""
    names = {
        "uz": "O'zbek tili",
        "ru": "Русский",
        "en": "English"
    }
    return names.get(code, "English")

