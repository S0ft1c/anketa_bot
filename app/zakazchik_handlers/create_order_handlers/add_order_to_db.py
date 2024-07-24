from sqlite_database import DB
from loguru import logger


async def add_order_to_db(tg_id: str, data: dict):
    try:
        async with DB() as db:
            await db.insert_order(
                customer_id=tg_id,
                date=data['date'],
                how_many_ppl=data['how_many_ppl'],
                address=data['address'],
                work_desc=data['work_desc'],
                payment=data['payment'],
                help_phone=data['help_phone'],
                full_address=data['FULL_address'],
                full_work_desc=data['FULL_work_desc'],
                full_phones=data['FULL_phones'],
                full_additional_info=data['FULL_additional_info'],
                long_time=data['long_time'],
                long_days=data.get('long_days', 0)
            )

    except Exception as e:
        logger.error(f'Error in add_order_to_db -> {e}')
