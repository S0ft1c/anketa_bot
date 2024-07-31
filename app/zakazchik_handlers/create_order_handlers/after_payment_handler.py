from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from aiogram.types import Message
from loguru import logger
from utils import validate_how_many_ppl

from .back_to_zakazhick_btn import back_to_zakazhick_btn
after_payment_router = Router()


@after_payment_router.message(CreateOrderStates.payment)
async def after_payment_handler(message: Message, state: FSMContext):
    try:
        if not validate_how_many_ppl(message.text):
            await message.answer(
                text='<b>Указание оплаты</b>\n\n'
                     '❌ Введенное вами значение некорректно! Попробуйте еще раз.',
                parse_mode=ParseMode.HTML,
                reply_markup=back_to_zakazhick_btn
            )
        else:
            # update data
            await state.update_data(payment=message.text)
            # set new state
            await state.set_state(CreateOrderStates.help_phone)

            # answer
            await message.answer(
                text='<b>Указанная оплата сохранена!</b> '
                     '<i>☎️ Теперь введите номер телефона для справок.</i>\n\n'
                     'Телефон для справок должен быть телефоном. Писать его надо в <u>международном формате</u>\n'
                     'Например вы можете указать что-то из:\n'
                     '<pre>+71234567890\n'
                     '+7 999 999 99 99\n'
                     '+7 999 999-99-99\n</pre>',
                parse_mode='HTML',
                reply_markup=back_to_zakazhick_btn
            )
    except Exception as e:
        logger.error(f'Error in after_payment_handler -> {e}')
