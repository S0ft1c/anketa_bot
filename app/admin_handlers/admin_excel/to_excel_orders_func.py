import pandas as pd
from aiogram import Bot
from loguru import logger
from aiogram.types.input_file import FSInputFile

from sqlite_database import DB


async def to_excel_orders_func(bot: Bot, chat_id: str | int, start_date: str, end_date: str):
    try:
        start_date = pd.to_datetime(start_date, format='%d.%m.%Y')
        end_date = pd.to_datetime(end_date, format='%d.%m.%Y')

        async with DB() as db:
            logs = await db.select_all_admin_logs()
        table = pd.DataFrame(logs)
        table['date'] = pd.to_datetime(table['date'], format='%H:%M %d.%m.%Y')

        table = table[
            (table['date'] >= start_date) & (table['date'] <= end_date)
            ]

        table = table[[
            'customer_id',
            'date',
            'how_many_ppl',
            'address',
            'work_desc',
            'payment',
            'help_phone',
            'FULL_address',
            'FULL_work_desc',
            'FULL_phones',
            'FULL_additional_info',
            'long_time',
            'long_days',
            'report'
        ]]
        table = table.drop_duplicates(inplace=False)
        table = table.rename(columns={
            'customer_id': 'ID заказчика',
            'date': 'Дата заказа',
            'how_many_ppl': 'Сколько надо людей',
            'address': 'Адрес',
            'work_desc': 'Специфика работы',
            'payment': 'Оплата в час',
            'help_phone': 'Телефон для справок',
            'FULL_address': 'Подробный адрес',
            'FULL_work_desc': 'Подробная специфика работы',
            'FULL_phones': 'Подробная информация о контактных лицах',
            'FULL_additional_info': 'Доп. информация',
            'long_time': 'Является ли заказ долгосрочным',
            'long_days': 'Сколько дней занимает долгосрочный заказ'
        })
        table.to_excel('output.xlsx', index=False)

        await bot.send_document(
            chat_id=chat_id,
            caption='Вот ваша выгрузка по заказам!',
            document=FSInputFile('output.xlsx'),
        )

    except Exception as e:
        logger.error(f'Error in to_excel_orders_func: {e}')
