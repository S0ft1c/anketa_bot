from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger
from .back_to_zakazhick_btn import back_to_zakazhick_btn

yes_long_time_router = Router()


@yes_long_time_router.callback_query(F.data.contains('yes_long_time'), CreateOrderStates.long_time)
async def yes_long_time(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer('')
        await state.update_data(long_time=True)
        await state.set_state(CreateOrderStates.long_days)

        await callback.message.answer(
            text='<b>Создание долгосрочного заказа!</b> '
                 '<i>Итак, вы создаете долгосрочный заказ. Укажите сколько дней он будет длиться</i>\n\n'
                 'Если вы не знаете точно, то можно '
                 'указать 0 и тогда заказ будет выполняться до того момента, как его отменит администратор',
            parse_mode='HTML',
            reply_markup=back_to_zakazhick_btn,
        )

    except Exception as e:
        logger.error(f'Error in yes_long_time -> {e}')
