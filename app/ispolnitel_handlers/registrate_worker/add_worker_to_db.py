from loguru import logger

from sqlite_database import DB


async def add_worker_to_db(tg_id: int | str, tg_nickname: str, data: dict):
    try:
        async with DB() as db:
            await db.insert_worker(
                telegram_id=tg_id,
                full_name=data['fio'],
                contact_number=data['contact_number'],
                tg_nickname=tg_nickname,
                date_of_birth=data['date_of_birth'],
                area_of_residence=data['area_of_residence'],
            )
    except Exception as e:
        logger.error(f'Error in add_worker_to_db -> {e}')
