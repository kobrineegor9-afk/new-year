from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = '📝 мои напоминания ')],
            [KeyboardButton(text = '➕ добавить'),
             KeyboardButton(text='❌ удалить ')],
            [KeyboardButton(text = '🗑 очистить все'),
             KeyboardButton(text='ℹ️ помощь')]
        ],
        resize_keyboard = True
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