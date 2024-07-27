from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB
from .try_to_up_rating import try_to_update_rating

admin_submit_hours_commit_router = Router()


@admin_submit_hours_commit_router.callback_query(F.data.contains('admin_submit_hours_commit'))
async def admin_submit_hours_commit_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')
        review_id, conted_hours = callback.data.split('=')[1:]

        async with DB() as db:
            rev_info = await db.select_review_by_id(review_id)

            lastrowid = await db.insert_admin_log(
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
                hours=conted_hours,
            )
            await db.delete_review_by_id(review_id=review_id)

        await try_to_update_rating(rev_info)

        await callback.message.answer(
            text=f'<b>Количество часов для пользователя подтверждено!</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Перейти к списку',
                                      callback_data='admin_hours_commit_list')]
            ])
        )
    except Exception as e:
        logger.error(f'Error in admin_submit_hours_commit: {e}')
