import asyncio

from aiogram import Bot
from aiogram.enums import ParseMode
from loguru import logger

from sqlite_database import DB


async def repeat_long_time_order(
        bot: Bot,
        customer_id: int | str,
        workers_ids: list[str | int],
        date: str,
        how_many_ppl: int,
        address: str,
        work_desc: str,
        payment: int,
        help_phone: str,
        full_address: str,
        full_work_desc: str,
        full_phones: str,
        full_additional_info: str,
        long_time: bool,
        long_days: int,
):
    try:
        async with DB() as db:
            # add to the orders for visibility of the orderer
            order_id = await db.insert_order(
                customer_id=customer_id,
                date=date,
                how_many_ppl=how_many_ppl,
                address=address,
                work_desc=work_desc,
                payment=payment,
                help_phone=help_phone,
                full_address=full_address,
                full_work_desc=full_work_desc,
                full_phones=full_phones,
                full_additional_info=full_additional_info,
                long_time=long_time,
                long_days=long_days,
            )

            # for every worker add to inworks
            for worker_id in workers_ids:
                await db.insert_inwork(
                    worker_id=worker_id,
                    order_id=order_id,
                )

        # send a message to a customer
        await bot.send_message(
            chat_id=customer_id,
            text='<b>Ваш долгосрочный заказ вновь появился!</b>\n'
                 'Теперь ваш долгосрочный заказ доступен в разделе "Мои заказы". '
                 'Все исполнители, что были на предыдущем дне заказа также были проинформированы.',
            parse_mode=ParseMode.HTML,
        )
        await asyncio.sleep(5)

        # send message to all workers
        for worker_id in workers_ids:
            await bot.send_message(
                chat_id=worker_id,
                text='<b>Долгосрочный заказ был добавлен к вам в "Активные заказы".</b> '
                     'Не забудьте явится и сделать его!',
                parse_mode=ParseMode.HTML,
            )
            await asyncio.sleep(5)

    except Exception as e:
        logger.error(f'Error in repeat_long_time_order: {e}')
