from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    """Главная клавиатура"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Мои напоминания")],
            [KeyboardButton(text="➕ Добавить"),
             KeyboardButton(text="❌ Удалить")],
            [KeyboardButton(text="🗑 Очистить всё"),
             KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_reminder_actions_keyboard():
    """Клавиатура для действий с напоминанием"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Удалить"),
             KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    return keyboard