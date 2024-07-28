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
            await db.insert_admin_log(
                customer_id=rev_info['customer_id'],
                worker_id=rev_info['worker_id'],
                date=rev_info['date'],
                how_many_ppl=rev_info['how_many_ppl'],
                address=rev_info['address'],
                work_desc=rev_info['work_desc'],
                payment=rev_info['payment'],
                help_phone=rev_info['help_phone'],
                full_address=rev_info['FULL_address'],
                full_work_desc=rev_info['FULL_work_desc'],
                full_phones=rev_info['FULL_phones'],
                full_additional_info=rev_info['FULL_additional_info'],
                long_time=rev_info['long_time'],
                long_days=rev_info['long_days'],
                report=rev_info['report'],
                hours=-1,
            )
            await db.delete_review_by_id(rev_id)

        await callback.message.answer(
            text='<b>Отсутствие исполнителя на заказе отмечено</b>',
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        logger.error(f'Error in admin_minus_worker_handler: {e}')
