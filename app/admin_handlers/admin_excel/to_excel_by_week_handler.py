from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from .get_all_data_to_excel_func import get_all_data_to_excel

to_excel_by_week_router = Router()


def get_previous_friday():
    today = datetime.today()
    offset = (today.weekday() - 4) % 7
    last_friday = today - timedelta(days=offset)
    last_friday = last_friday.strftime("%d.%m.%Y")
    return last_friday


def get_upcoming_friday():
    today = datetime.today()
    offset = (4 - today.weekday()) % 7
    if offset == 0:  # Если сегодня пятница, вернуть текущую дату
        upcoming_friday = today
    else:
        upcoming_friday = today + timedelta(days=offset)
    upcoming_friday = upcoming_friday.strftime("%d.%m.%Y")
    return upcoming_friday


@to_excel_by_week_router.callback_query(F.data.contains('to_excel_by_week'))
async def to_excel_by_week_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()

        last_friday = get_previous_friday()
        cur_friday = get_upcoming_friday()

        await get_all_data_to_excel(
            bot=callback.bot,
            chat_id=callback.from_user.id,
            start_date=last_friday,
            end_date=cur_friday,
        )

    except Exception as e:
        logger.error(f'Error in to_excel_by_week_handler: {e}')
