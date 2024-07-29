import pandas as pd
from aiogram import Bot
from aiogram.types.input_file import FSInputFile
from loguru import logger

from sqlite_database import DB


async def get_all_data_to_excel(bot: Bot, chat_id: int | str, start_date: str, end_date: str):
    try:
        start_date = pd.to_datetime(start_date, format='%d.%m.%Y')
        end_date = pd.to_datetime(end_date, format='%d.%m.%Y')

        async with DB() as db:
            logs = await db.select_all_admin_logs()
        table = pd.DataFrame(logs)
        table['date'] = pd.to_datetime(table['date'], format='%H:%M %d.%m.%Y')
        # print(table['date'])
        # print(start_date, end_date)

        table = table[
            (table['date'] >= start_date) & (table['date'] <= end_date)
            ]

        table['weekday'] = table['date'].dt.day_name()
        table['date'] = table['date'].dt.date
        table['Дата'] = table['date'].astype(str) + '|' + table['weekday']

        table['Telegram ID работника'] = table['worker_id']
        table['Оплата (руб/час)'] = table['payment']
        table['Адрес'] = table['address']
        table['Описание работы'] = table['work_desc']
        table['Количество отработанных часов'] = table['hours']
        pivot_table = \
            pd.pivot_table(
                table,
                values=['Оплата (руб/час)', 'Адрес', 'Описание работы', 'Количество отработанных часов'],
                index='Telegram ID работника',
                columns='Дата',
                aggfunc={
                    'Оплата (руб/час)': 'sum',
                    'Адрес': 'first',
                    'Описание работы': 'first',
                    'Количество отработанных часов': 'first',
                },
                fill_value=0
            )
        pivot_table = pivot_table.swaplevel(axis=1).sort_index(axis=1, level=0)

        # print(pivot_table)
        pivot_table.to_excel('output.xlsx')
    except Exception as e:
        logger.error(f'Error in creating the pivot -> {e}')

    try:

        await bot.send_document(
            chat_id=chat_id,
            caption='Вот ваша выгрузка!',
            document=FSInputFile('output.xlsx'),
        )

    except Exception as e:
        logger.error(f'Error in sending a excel file -> {e}')
