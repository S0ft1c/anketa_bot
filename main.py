from dotenv import load_dotenv
import os
import asyncio
from aiogram import Bot, Dispatcher
from app import router
from loguru import logger

load_dotenv()
TOKEN = os.environ.get('TOKEN')


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # add the app router
    dp.include_router(router)
    logger.info('All routers included!')
    # start polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
