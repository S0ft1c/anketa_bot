from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger

yes_long_time_router = Router()


@yes_long_time_router.callback_query(F.data.contains('yes_long_time'), CreateOrderStates.long_time)
async def yes_long_time(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer('')
        await state.update_data(long_time=True)
        await state.set_state(CreateOrderStates.long_days)

        await callback.message.answer(
            text='<b>Создание долгосрочного заказа заказа.</b>'
                 'Теперь введите количество дней, сколько будет длится заказ. Если вы не знаете точно, то можно '
                 'указать 0 и тогда заказ будет выполняться до того момента, как его отменит администратор',
            parse_mode='HTML',
        )

    except Exception as e:
        logger.error(f'Error in yes_long_time -> {e}')
