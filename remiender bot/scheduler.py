import asyncio
import logging
from datetime import datetime
from aiogram import Bot
from database import get_pending_reminders, mark_reminder_as_sent


async def check_reminders(bot: Bot):
    """Фоновая задача для проверки и отправки напоминаний"""
    while True:
        try:
            # Получаем все просроченные напоминания
            reminders = get_pending_reminders()

            for reminder_id, user_id, text, reminder_datetime in reminders:
                try:
                    # Отправляем напоминание
                    await bot.send_message(
                        user_id,
                        f"⏰ *НАПОМИНАНИЕ!*\n\n"
                        f"📝 {text}\n\n"
                        f"🕐 Запланировано на: {reminder_datetime}",
                        parse_mode="Markdown"
                    )

                    # Отмечаем как отправленное
                    mark_reminder_as_sent(reminder_id)
                    logging.info(f"Отправлено напоминание {reminder_id} пользователю {user_id}")

                except Exception as e:
                    logging.error(f"Ошибка при отправке напоминания {reminder_id}: {e}")

            # Проверяем каждые 30 секунд
            await asyncio.sleep(30)

        except Exception as e:
            logging.error(f"Ошибка в планировщике: {e}")
            await asyncio.sleep(60)


async def start_scheduler(bot: Bot):
    """Запуск планировщика"""
    asyncio.create_task(check_reminders(bot))
    logging.info("Планировщик напоминаний запущен")