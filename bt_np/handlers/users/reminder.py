from datetime import datetime
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from loader import router
from database import (
    add_reminder, get_user_reminders, delete_reminder,
    delete_all_reminders, get_reminder_by_id
)
from keyboards.reply import get_main_keyboard, get_reminder_actions_keyboard


# Состояния для FSM
class ReminderStates(StatesGroup):
    waiting_text = State()
    waiting_date = State()
    waiting_time = State()
    waiting_delete_id = State()


@router.message(lambda message: message.text == "📝 Мои напоминания")
async def show_reminders(message: Message):
    user_id = message.from_user.id
    reminders = get_user_reminders(user_id)

    if not reminders:
        await message.answer(
            "📭 У тебя пока нет напоминаний!\n\n"
            "Создай первое напоминание через кнопку ➕ Добавить",
            reply_markup=get_main_keyboard()
        )
        return

    response = "📝 *Твои напоминания:*\n\n"

    for i, reminder in enumerate(reminders, 1):
        reminder_id, text, reminder_datetime, created_at = reminder
        # Форматируем дату
        try:
            dt = datetime.strptime(reminder_datetime, "%Y-%m-%d %H:%M:%S")
            formatted_date = dt.strftime("%d.%m.%Y в %H:%M")
        except:
            formatted_date = reminder_datetime

        response += f"{i}. *ID:{reminder_id}*\n"
        response += f"   📝 {text}\n"
        response += f"   ⏰ {formatted_date}\n\n"

    response += "Чтобы удалить напоминание, нажми ❌ Удалить"

    await message.answer(response, parse_mode="Markdown", reply_markup=get_main_keyboard())


@router.message(lambda message: message.text == "➕ Добавить")
async def add_reminder_start(message: Message, state: FSMContext):
    await message.answer(
        "✏️ Напиши текст напоминания:\n\n"
        "Пример: 'Позвонить маме' или 'Купить хлеб'",
        reply_markup=get_main_keyboard()
    )
    await state.set_state(ReminderStates.waiting_text)


@router.message(ReminderStates.waiting_text)
async def add_reminder_text(message: Message, state: FSMContext):
    if len(message.text) > 200:
        await message.answer("❌ Текст слишком длинный! Максимум 200 символов. Попробуй снова:")
        return

    await state.update_data(text=message.text)

    await message.answer(
        "📅 Введи *дату* напоминания в формате:\n\n"
        "`ДД.ММ.ГГГГ`\n\n"
        "Пример: `25.12.2024`",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
    await state.set_state(ReminderStates.waiting_date)


@router.message(ReminderStates.waiting_date)
async def add_reminder_date(message: Message, state: FSMContext):
    date_str = message.text.strip()

    try:
        # Парсим дату
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")

        # Проверяем, что дата не в прошлом
        if date_obj.date() < datetime.now().date():
            await message.answer(
                "❌ Нельзя создать напоминание в прошлом!\n"
                "Введи будущую дату:",
                reply_markup=get_main_keyboard()
            )
            return

        await state.update_data(date=date_str)

        await message.answer(
            "⏰ Введи *время* напоминания в формате:\n\n"
            "`ЧЧ:ММ` (24-часовой формат)\n\n"
            "Пример: `14:30`",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        await state.set_state(ReminderStates.waiting_time)

    except ValueError:
        await message.answer(
            "❌ Неправильный формат даты!\n"
            "Используй формат: `ДД.ММ.ГГГГ`\n"
            "Пример: `25.12.2024`",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )


@router.message(ReminderStates.waiting_time)
async def add_reminder_time(message: Message, state: FSMContext):
    time_str = message.text.strip()

    try:
        # Парсим время
        time_obj = datetime.strptime(time_str, "%H:%M")

        data = await state.get_data()
        date_str = data.get('date')
        text = data.get('text')

        # Объединяем дату и время
        datetime_str = f"{date_str} {time_str}:00"
        reminder_datetime = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M:%S")

        # Проверяем, что дата+время не в прошлом
        if reminder_datetime < datetime.now():
            await message.answer(
                "❌ Нельзя создать напоминание в прошлом!\n"
                "Введи будущее время:",
                reply_markup=get_main_keyboard()
            )
            return

        # Сохраняем напоминание
        reminder_id = add_reminder(
            message.from_user.id,
            text,
            reminder_datetime.strftime("%Y-%m-%d %H:%M:%S")
        )

        formatted_datetime = reminder_datetime.strftime("%d.%m.%Y в %H:%M")

        await message.answer(
            f"✅ *Напоминание создано!*\n\n"
            f"📝 {text}\n"
            f"⏰ {formatted_datetime}\n"
            f"🆔 ID: {reminder_id}\n\n"
            f"Я напомню тебе вовремя! ⏰",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Неправильный формат времени!\n"
            "Используй формат: `ЧЧ:ММ`\n"
            "Пример: `14:30`",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )


@router.message(lambda message: message.text == "❌ Удалить")
async def delete_reminder_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    reminders = get_user_reminders(user_id)

    if not reminders:
        await message.answer(
            "📭 У тебя нет активных напоминаний!",
            reply_markup=get_main_keyboard()
        )
        return

    # Показываем список напоминаний для удаления
    response = "🗑 *Выбери напоминание для удаления:*\n\n"
    for reminder in reminders:
        reminder_id, text, reminder_datetime, _ = reminder
        response += f"ID: `{reminder_id}` - {text}\n"

    response += "\nОтправь *ID* напоминания, которое хочешь удалить:"

    await message.answer(response, parse_mode="Markdown", reply_markup=get_reminder_actions_keyboard())
    await state.set_state(ReminderStates.waiting_delete_id)


@router.message(ReminderStates.waiting_delete_id)
async def delete_reminder_by_id(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Главное меню:", reply_markup=get_main_keyboard())
        return

    try:
        reminder_id = int(message.text)

        # Проверяем, существует ли напоминание
        reminder = get_reminder_by_id(reminder_id)

        if not reminder or reminder[1] != message.from_user.id:
            await message.answer(
                "❌ Напоминание с таким ID не найдено!\n"
                "Попробуй снова или нажми 'Назад':",
                reply_markup=get_reminder_actions_keyboard()
            )
            return

        # Удаляем напоминание
        if delete_reminder(reminder_id, message.from_user.id):
            await message.answer(
                f"✅ Напоминание *ID: {reminder_id}* удалено!",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer("❌ Ошибка при удалении!", reply_markup=get_main_keyboard())

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Отправь число (ID напоминания)!\n"
            "Или нажми 'Назад':",
            reply_markup=get_reminder_actions_keyboard()
        )


@router.message(lambda message: message.text == "🗑 Очистить всё")
async def delete_all_reminders_handler(message: Message):
    user_id = message.from_user.id
    reminders = get_user_reminders(user_id)

    if not reminders:
        await message.answer(
            "📭 У тебя нет активных напоминаний!",
            reply_markup=get_main_keyboard()
        )
        return

    deleted = delete_all_reminders(user_id)

    await message.answer(
        f"🗑 Удалено *{deleted}* напоминаний!\n\n"
        f"Теперь твой список напоминаний пуст.",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


@router.message(lambda message: message.text == "ℹ️ Помощь")
async def show_help(message: Message):
    help_text = (
        "⏰ *Помощь по боту-напоминалке*\n\n"
        "📝 *Мои напоминания* - посмотреть все активные напоминания\n"
        "➕ *Добавить* - создать новое напоминание\n"
        "   • Сначала напиши текст\n"
        "   • Потом дату (ДД.ММ.ГГГГ)\n"
        "   • Потом время (ЧЧ:ММ)\n\n"
        "❌ *Удалить* - удалить конкретное напоминание по ID\n"
        "🗑 *Очистить всё* - удалить все напоминания\n\n"
        "💡 *Совет:* ID напоминания виден в списке 'Мои напоминания'\n\n"
        "Я напомню тебе в указанное время! ⏰"
    )
    await message.answer(help_text, parse_mode="Markdown", reply_markup=get_main_keyboard())