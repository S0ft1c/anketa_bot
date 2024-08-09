import asyncio
import os

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from loguru import logger

from sqlite_database import DB

load_dotenv()
bot_url = os.environ.get("BOT_URL")


async def send_message_to_worker(bot: Bot, order, worker):
    try:
        if order['long_time'] and order['long_days'] > 0:
            ll_txt = (f'<u>Это долгосрочный заказ. Его длительность = {order['long_days']}</u>\n'
                      f'Учитывайте дату, когда создавался заказ, чтобы понять до какого он числа.')
        elif order['long_time'] and order['long_days'] == 0:
            ll_txt = f'<u>Это долгосрочный заказ. Его длительность не была определена заказчиком.</u>'
        else:
            ll_txt = f'<u>Это не долгосрочный заказ.</u>'

        await bot.send_message(
            chat_id=worker['telegram_id'],
            text=f'<b>Вам доступен новый заказ!</b>\n'
                 f'📅 <b>Дата заказа: {order['date'].replace('.20', '.')}</b>\n--------------\n'
                 f'👥 <i>Людей надо</i>: {order['how_many_ppl']}\n--------------\n'
                 f'🏠 <i>Адрес</i>: {order['address']}\n--------------\n'
                 f'🔧 <i>Описание работы</i>\n{order['work_desc']}\n--------------\n'
                 f'💵 <i>Оплата (руб/час)</i> {order['payment']}\n--------------\n'
                 f'📞 <i>Телефон для справок</i>\n{order['help_phone']}\n--------------\n\n' + ll_txt,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Я приду!',
                                      callback_data=f'join_to_order_request={order['id']}')],
            ])
        )
    except Exception as e:
        logger.error(f'Error in schedulers.send_message_to_workers: {e}')


async def send_message_to_group(bot: Bot, order):
    try:
        load_dotenv()

        if order['long_time'] and order['long_days'] > 0:
            ll_txt = (f'<u>Это долгосрочный заказ. Его длительность = {order['long_days']}</u>\n'
                      f'Учитывайте дату, когда создавался заказ, чтобы понять до какого он числа.')
        elif order['long_time'] and order['long_days'] == 0:
            ll_txt = f'<u>Это долгосрочный заказ. Его длительность не была определена заказчиком.</u>'
        else:
            ll_txt = f'<u>Это не долгосрочный заказ.</u>'

        await bot.send_message(
            chat_id=os.environ.get('GROUP_ID'),
            text=f'<b>Вам доступен новый заказ!</b>\n'
                 f'📅 <b>Дата заказа: {order['date'].replace('.20', '.')}</b>\n--------------\n'
                 f'👥 <i>Людей надо</i>: {order['how_many_ppl']}\n--------------\n'
                 f'🏠 <i>Адрес</i>: {order['address']}\n--------------\n'
                 f'🔧 <i>Описание работы</i>\n{order['work_desc']}\n--------------\n'
                 f'💵 <i>Оплата (руб/час)</i> {order['payment']}\n--------------\n'
                 f'📞 <i>Телефон для справок</i>\n{order['help_phone']}\n--------------\n\n' + ll_txt,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Я приду!',
                                      url=f'{bot_url}?start={order["id"]}')],
            ])
        )
    except Exception as e:
        logger.error(f'Error in schedulers.send_message_to_group: {e}')


async def send_order_to_workers(bot: Bot, order_id: int | str):
    try:
        async with DB() as db:
            order = await db.select_order_by_id(order_id)
            workers = await db.get_all_workers()

        # green workers first
        for worker in workers['green']:
            await send_message_to_worker(bot, order, worker)
            await asyncio.sleep(5)

        await asyncio.sleep(10 * 60)  # wait for 10 minutes

        # yellow workers second
        for worker in workers['yellow']:
            await send_message_to_worker(bot, order, worker)
            await asyncio.sleep(5)

        await asyncio.sleep(15 * 60)  # wait for 15 minutes

        # red on the third (to group)
        await send_message_to_group(bot, order)

        logger.info(f'All workers got messages')
    except Exception as e:
        logger.error(f'Error in send_order_to_workers: {e}')
