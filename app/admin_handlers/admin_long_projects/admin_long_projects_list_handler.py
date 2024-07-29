from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB

admin_long_projects_list_router = Router()


async def create_kb(long_orders: list[dict]):
    builder = InlineKeyboardBuilder()
    for long_order in long_orders:
        builder.add(
            InlineKeyboardButton(
                text=f'{long_order['date']} -- {long_order['address']}',
                callback_data=f'admin_view_long_project={long_order["id"]}'
            )
        )
    return builder.adjust(1).as_markup()


@admin_long_projects_list_router.callback_query(F.data.contains('admin_long_projects_list'))
async def admin_long_projects_list_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()

        async with DB() as db:
            long_orders = await db.select_long_projects_from_orders()

        await callback.message.answer(
            text='Вот все долгосрочные проекты, количество дней которых было не указано',
            parse_mode=ParseMode.HTML,
            reply_markup=await create_kb(long_orders),
        )

    except Exception as e:
        logger.error(f'Error in admin_long_projects_list_handler: {e}')
