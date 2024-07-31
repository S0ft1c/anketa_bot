from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from utils import is_valid_datetime
from .back_to_zakazhick_btn import back_to_zakazhick_btn
from .create_order_states import CreateOrderStates

after_date_router = Router()


@after_date_router.message(CreateOrderStates.date)
async def after_date_hander(message: Message, state: FSMContext):
    try:
        if not is_valid_datetime(message.text):
            await message.answer(
                text='<b> 📅 Указание даты выполнения заказа.</b>\n\n'
                     '❌ Введенная вами дата некорректна. Попробуйте еще раз.',
                parse_mode='HTML',
                reply_markup=back_to_zakazhick_btn
            )
        else:
            # update the info
            await state.update_data(date=message.text)
            # update the StatesGroup
            await state.set_state(CreateOrderStates.how_many_ppl)

            # answer
            await message.answer(
                text='<b>Отправленная вами дата сохранена!</b> '
                     '<i>🧑‍🏭 Теперь введите сколько людей надо для работы.</i>\n\n'
                     'Введите ТОЛЬКО число. Например: <pre>2</pre>',
                parse_mode='HTML',
                reply_markup=back_to_zakazhick_btn
            )
    except Exception as e:
        logger.error(f'Error in after_date_handler -> {e}')
