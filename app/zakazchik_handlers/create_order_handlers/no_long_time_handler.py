from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger
from .add_order_to_db import add_order_to_db

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

        await add_order_to_db(
            str(callback.from_user.id),
            await state.get_data()
        )
        await state.clear()
    except Exception as e:
        logger.error(f'Error in yes_long_time -> {e}')
