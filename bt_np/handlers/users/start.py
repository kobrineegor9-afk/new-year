from aiogram.filters import Command
from aiogram.types import Message
from loader import router
from database import register_user
from keyboards.reply import get_main_keyboard


@router.message(Command('start'))
async def cmd_start(message: Message):
    # Регистрируем пользователя
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    register_user(user_id, username)

    await message.answer(
        f"⏰ Привет, {message.from_user.first_name}!\n\n"
        "Я бот-напоминалка. Вот что я умею:\n\n"
        "📝 *Мои напоминания* - посмотреть все напоминания\n"
        "➕ *Добавить* - создать новое напоминание\n"
        "❌ *Удалить* - удалить конкретное напоминание\n"
        "🗑 *Очистить всё* - удалить все напоминания\n"
        "ℹ️ *Помощь* - показать это сообщение\n\n"
        "Создай своё первое напоминание прямо сейчас! 🎯",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )