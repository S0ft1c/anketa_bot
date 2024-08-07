import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from loguru import logger

from app import router
from schedulers import scheduler

load_dotenv()
TOKEN = os.environ.get('TOKEN')


async def main():
    # configure logger
    logger.add("test_dir/bot.log", format="{time} {level} {message}", level="INFO")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # add the app router
    dp.include_router(router)
    logger.info('All routers included!')

    # start scheduler
    scheduler.start()

    # start polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
