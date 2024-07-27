from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from sqlite_database import DB

admin_minus_worker_router = Router()


@admin_minus_worker_router.callback_query(F.data.contains('admin_minus_worker'))
async def admin_minus_worker_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')
        rev_id = callback.data.split('=')[-1]

        async with DB() as db:
            rev_info = await db.select_review_by_id(rev_id)
            await db.decrease_worker_rating(rev_info['worker_id'])
            await db.delete_review_by_id(rev_id)

        await callback.message.answer(
            text='<b>Отсутствие исполнителя на заказе отмечено</b>',
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        logger.error(f'Error in admin_minus_worker_handler: {e}')
