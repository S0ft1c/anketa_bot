from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB
from utils import validate_long_days
from .try_to_up_rating import try_to_update_rating


class SelfHoursCommitStates(StatesGroup):
    hours = State()


admin_self_hours_commit_router = Router()


@admin_self_hours_commit_router.callback_query(F.data.contains('admin_self_hours_commit'))
async def admin_self_hours_commit_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        review_id = callback.data.split('=')[-1]
        await state.update_data(rev_id=review_id)
        await state.set_state(SelfHoursCommitStates.hours)
        await callback.answer('')

        await callback.message.answer(
            text=f'Введите число часов, которые вы проставляете исполнителю.\n'
                 f'Это обязательно должно быть число',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Назад',
                                      callback_data='admin_hours_commit_list')]
            ])
        )

    except Exception as e:
        logger.error(f'Error in admin_self_hours_commit_handler: {e}')


@admin_self_hours_commit_router.message(SelfHoursCommitStates.hours)
async def admin_hours_commit_handler(message: Message, state: FSMContext):
    try:
        rev_data = await state.get_data()
        rev_id = rev_data.get('rev_id')
        if validate_long_days(message.text):
            await state.clear()
            async with DB() as db:
                rev_info = await db.select_review_by_id(rev_id)
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
                    hours=message.text,
                )
                await db.delete_review_by_id(review_id=rev_id)

            await try_to_update_rating(rev_info)

            await message.answer(
                text=f'<b>Количество часов для пользователя выставлено!</b>',
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Перейти к списку',
                                          callback_data='admin_hours_commit_list')]
                ])
            )
        else:
            await message.answer(
                text='Введенное вами значение некорректно! Попробуйте еще раз.'
            )
    except Exception as e:
        logger.error(f'Error in admin_self_hours_commit_handler: {e}')
