from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB

admin_hours_commit_list_router = Router()


async def create_kb():
    builder = InlineKeyboardBuilder()
    async with DB() as db:
        revs = await db.select_all_admin_reviews()
        for el in revs:
            builder.add(
                InlineKeyboardButton(
                    text=f'Дата заказа - {el['date']}',
                    callback_data=f'view_review_id={el['id']}'
                )
            )
    return builder.adjust(1).as_markup()


@admin_hours_commit_list_router.callback_query(F.data.contains('admin_hours_commit_list'))
async def admin_hours_commit_list_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')

        await callback.message.answer(
            text=f'<b>Список всех выполненных заказов на принятие отдельно по каждому человеку.</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=await create_kb(),
        )

    except Exception as e:
        logger.error(f'Error in admin_hours_commit_list_handler: {e}')
