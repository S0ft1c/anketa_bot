from aiogram import Router
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from aiogram.types import Message
from loguru import logger
from utils import validate_how_many_ppl

after_payment_router = Router()


@after_payment_router.message(CreateOrderStates.payment)
async def after_payment_handler(message: Message, state: FSMContext):
    try:
        if not validate_how_many_ppl(message.text):
            await message.answer(
                text='<b>Создание нового заказа</b>\n\n'
                     'Введенное вами значение некорректно! Попробуйте еще раз.'
            )
        else:
            # update data
            await state.update_data(payment=message.text)
            # set new state
            await state.set_state(CreateOrderStates.help_phone)

            # answer
            await message.answer(
                text='<b>Создание нового заказа</b>\n\n'
                     'Указанная оплата сохранена! Теперь введите номер телефона для справок.',
                parse_mode='HTML',
            )
    except Exception as e:
        logger.error(f'Error in after_payment_handler -> {e}')
