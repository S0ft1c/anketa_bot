from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from loguru import logger
from sqlite_database import DB

list_my_orders_router = Router()


async def create_kb(orders: dict):
    builder = InlineKeyboardBuilder()
    for el in orders:
        builder.add(
            InlineKeyboardButton(text=f'{el['date']} - {el['address']}',
                                 callback_data=f'view_order_by_id={el['id']}')
        )
    builder.add(
        InlineKeyboardButton(text='🔙 Назад', callback_data='ya_zakazchik')
    )
    return builder.adjust(1).as_markup()


@list_my_orders_router.callback_query(F.data.contains('view_my_orders'))
async def view_my_orders_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        async with DB() as db:
            orders = await db.select_orders_where_customer(callback.from_user.id)

        await callback.answer('')
        await callback.message.answer(
            text='<b>Ваши заказы.</b>\n'
                 'Ниже представлены все ваши заказы.',
            parse_mode='HTML',
            reply_markup=await create_kb(orders)
        )

    except Exception as e:
        logger.error(f'Error in view_my_orders_handler -> {e}')
