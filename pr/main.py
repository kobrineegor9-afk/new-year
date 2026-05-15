import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.models import init_db
from handlers import admin, user
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from keyboards.inline import  kb_join

async def main():
    init_db()

    bot =Bot(token= BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())