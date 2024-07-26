from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from sqlite_database import DB
from utils import create_now_time_text

start_work_on_order_router = Router()


@start_work_on_order_router.callback_query(F.data.contains('start_work_on_order'))
async def start_work_on_order(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')
        order_id = callback.data.split('=')[-1]

        async with DB() as db:
            lastrowid = await db.update_start_date_inwork(
                worker_id=callback.from_user.id,
                order_id=order_id,
                start_time=await create_now_time_text(),
            )

        await callback.message.answer(
            text='Хорошо. Вы начали работать над заказом. Теперь в вашем меню "Активные заказы" в заказе, '
                 'который вы начали выполнять появилась кнопка "Я завершил работу". Нажмите ее только после того как '
                 'вы действительно завершите работу над заказом, потому что <b>опять начать работу будет невозможно</b>',
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(f'Error in start_work_on_order: {e}')
