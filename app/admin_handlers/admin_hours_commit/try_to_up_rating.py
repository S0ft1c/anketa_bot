from sqlite_database import DB
from loguru import logger

async def try_to_update_rating(rev_info: dict):
    try:
        async with DB() as db:
            worker_logs = await db.select_admin_logs_by_worker_id(rev_info['worker_id'])
            podryad = 0
            for log in worker_logs:
                if log['hours'] != -1:
                    podryad += 1
            if podryad % 7 == 0:
                await db.update_worker_rating(rev_info['worker_id'])
    except Exception as e:
        logger.error(f'Error in try_to_update_rating: {e}')