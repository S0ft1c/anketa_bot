import pandas as pd
from aiogram import Bot
from aiogram.types.input_file import FSInputFile
from loguru import logger

from sqlite_database import DB


async def to_excel_all_workers_func(bot: Bot, chat_id: str | int):
    try:

        async with DB() as db:
            workers = await db.get_all_workers(rated=False)

        table = pd.DataFrame(workers)
        table.rename(columns={
            'telegram_id': 'Телеграм ID',
            'full_name': 'ФИО',
            'contact_number': 'Контактный номер',
            'tg_nickname': 'Ник в ТГ',
            'date_of_birth': 'Дата рождения',
            'area_of_residence': 'Район проживания',
            'rating': 'Рейтинг'
        }, inplace=True)

        table.to_excel('output.xlsx', index=False)

        await bot.send_document(
            chat_id=chat_id,
            caption='Вот ваша выгрузка!',
            document=FSInputFile('output.xlsx')
        )

    except Exception as e:
        logger.error(f'Error in to_excel_all_workers_func: {e}')
