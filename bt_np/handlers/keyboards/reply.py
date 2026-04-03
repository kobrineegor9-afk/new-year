from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [keyboardbutton(text = '')]
        ]
    )
