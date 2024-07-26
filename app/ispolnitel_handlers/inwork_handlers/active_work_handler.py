from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB

active_work_router = Router()


async def create_kb(inworks: list) -> InlineKeyboardMarkup:
    async with DB() as db:
        orders_infos = [
            await db.select_order_by_id(order_id=el['order_id'])
            for el in inworks
        ]
        rr = []
        for el in orders_infos:
            rr.append(
                [InlineKeyboardButton(text=f'{el['date']} - {el['address']}',
                                      callback_data=f'worker_look_in_orderid={el['id']}')]
            )
        return InlineKeyboardMarkup(inline_keyboard=rr)


@active_work_router.callback_query(F.data.contains('active_work'))
async def active_work_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')

        async with DB() as db:
            active_work = await db.select_all_inwork_by_worker_id(callback.from_user.id)

        await callback.message.answer(
            text=f'Вот все ваши активные заказы',
            reply_markup=await create_kb(active_work)
        )

    except Exception as e:
        logger.error(f'Error in active_work handler: {e}')
