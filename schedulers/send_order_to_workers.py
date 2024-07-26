import asyncio

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from sqlite_database import DB


async def send_message_to_worker(bot: Bot, order, worker):
    try:
        await bot.send_message(
            chat_id=worker['telegram_id'],
            text=f'<b>Вам доступен новый заказ!</b>\n'
                 f'Дата: {order['date']}\n'
                 f'Требуется людей: {order['how_many_ppl']}\n'
                 f'Адрес: {order['address']}\n'
                 f'Описание работы:\n{order['work_desc']}\n'
                 f'Оплата (руб/час): {order['payment']}\n'
                 f'Телефон для справок: {order['help_phone']}\n'
                 f'{f'<u>Это долгосрочный заказ. => Сроки {order['long_days']} дн.</u>' if order['long_time']
                 else f'Это не долгосрочный заказ.'}',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Я приду!',
                                      callback_data=f'join_to_order_request={order['id']}')],
            ])
        )
    except Exception as e:
        logger.error(f'Error in schedulers.send_message_to_workers: {e}')


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

        # red on the third
        # TODO: send to the group
        for worker in workers['red']:
            await send_message_to_worker(bot, order, worker)
            await asyncio.sleep(5)

        logger.info(f'All workers got messages')
    except Exception as e:
        logger.error(f'Error in send_order_to_workers: {e}')
