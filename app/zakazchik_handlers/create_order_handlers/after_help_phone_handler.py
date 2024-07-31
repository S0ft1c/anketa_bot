from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from utils import is_valid_phone_number
from .create_order_states import CreateOrderStates
from .back_to_zakazhick_btn import  back_to_zakazhick_btn

after_help_phone_router = Router()


@after_help_phone_router.message(CreateOrderStates.help_phone)
async def after_help_phone_handler(message: Message, state: FSMContext):
    try:
        if not is_valid_phone_number(message.text):
            await message.answer(
                text='<b>Указание телефона.</b>\n\n'
                     '❌ Введенный вами номер не подходит! Вводите его в международном формате.',
                parse_mode=ParseMode.HTML,
                reply_markup=back_to_zakazhick_btn
            )
        else:
            # update
            await state.update_data(help_phone=message.text)
            # set new state
            await state.set_state(CreateOrderStates.FULL_address)

            # answer
            await message.answer(
                text='<b>Номер телефона сохранен!</b> <i>Приступаем к указанию подробной информации</i>\n\n'
                     'Напоминаем, что тут надо указывать абсолютно все данные, которые потребуются для исполнителя.\n'
                     'В подробной информации все пишется в свободной форме. Не стесняйтесь указывать необходимую '
                     'информацию.\n'
                     'Эту информацию получит исключительно исполнитель, который откликнулся на ваш заказ.\n'
                     '🏘 Итак, приступим. Укажите полностью адрес, куда надо прибыть исполнителю.',
                parse_mode='HTML',
                reply_markup=back_to_zakazhick_btn
            )

    except Exception as e:
        logger.error(f'Error in after_help_phone -> {e}')
