from aiogram import Router, F
from aiogram.types import CallbackQuery
from loguru import logger
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from .back_to_zakazhick_btn import back_to_zakazhick_btn

create_order_router = Router()


@create_order_router.callback_query(F.data.contains('create_order'))
async def create_order_callback_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer('')
        await state.set_state(CreateOrderStates.date)  # update state
        await callback.message.answer(
            text='<b>Создание нового заказа. 📅 Указание даты выполнения заказа.</b>\n\n'
                 '<i>Прекрасно.</i> Перейдем к созданию нового заказа.\n'
                 'Введете дату, когда нужно будет выполнить заказ. Дату надо указать в строгом формате:\n'
                 '<pre>час:минута день.месяц.год</pre>\n'
                 'Как пример вы должны написать - 19:30 01.04.2000.',
            parse_mode='HTML',
            reply_markup=back_to_zakazhick_btn,
        )
    except Exception as e:
        logger.error(f'Error in create_order_callback_handler -> {e}')
