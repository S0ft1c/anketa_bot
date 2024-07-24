from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from apscheduler.triggers.date import DateTrigger
from loguru import logger

from schedulers import scheduler, send_order_to_workers
from .add_order_to_db import add_order_to_db
from .create_order_states import CreateOrderStates

no_long_time_router = Router()


@no_long_time_router.callback_query(F.data.contains('no_long_time'), CreateOrderStates.long_time)
async def yes_long_time(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer('')
        await state.update_data(long_time=False)
        await state.set_state(CreateOrderStates.long_days)

        await callback.message.answer(
            text='<b>Создание заказа завершено!</b>'
                 'Вы можете увидеть свой заказ в разделе "Мои заказы"',
            parse_mode='HTML',
        )

        lastrowid = await add_order_to_db(
            str(callback.from_user.id),
            await state.get_data()
        )
        await state.clear()

        run_date = datetime.now() + timedelta(minutes=1)
        scheduler.add_job(
            func=send_order_to_workers,
            kwargs={'bot': callback.bot, 'order_id': lastrowid},
            trigger=DateTrigger(run_date=run_date),
        )
    except Exception as e:
        logger.error(f'Error in yes_long_time -> {e}')
