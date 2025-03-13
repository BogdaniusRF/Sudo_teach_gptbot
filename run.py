import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.user import user
from app.admin import admin
from app.database.models import async_main


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(user,admin)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


async def on_startup(dispatcher: Dispatcher):  # когда бот будет стартовать - всегда будут создаваться таблицы
    await async_main()  # когда бот будет стартовать - всегда будут создаваться таблицы


if __name__ == '__main__':
    try:
        asyncio.run(main())


    except KeyboardInterrupt:
        pass
