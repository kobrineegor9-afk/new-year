import asyncio
import logging
from loader import bot, dp
from scheduler import start_scheduler
from handlers.users import start
import handlers.users.reminder
async def main():
    logging.info('Бот - напоминалка запущен!')
    await start_scheduler(bot)
    await dp.start_polling(bot,
                           allowed_updates = dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run((main()))