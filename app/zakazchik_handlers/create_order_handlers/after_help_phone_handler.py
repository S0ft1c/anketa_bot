from aiogram import Router
from aiogram.types import Message
from .create_order_states import CreateOrderStates
from aiogram.fsm.context import FSMContext
from loguru import logger
from utils import is_valid_phone_number

after_help_phone_router = Router()

@after_help_phone_router.message(CreateOrderStates.help_phone)
async def after_help_phone_handler(message: Message, state: FSMContext):
    try:
        if not is_valid_phone_number(message.text):
            await message.answer(
                text='<b>Создание нового заказа</b>\n\n'
                     'Введенный вами номер не подходит! Вводите его в международном формате.'
            )
        else:
            # update
            await state.update_data(help_phone=message.text)
            # set new state
            await state.set_state(CreateOrderStates.FULL_address)

            # answer
            await message.answer(
                text='<b>Создание нового заказа. Добавление подробной информации</b>\n\n'
                     '<i>Прекрасно!</i> Теперь приступаем к вводу подробной информации.'
                     'Здесь надо указывать все полностью, так как эта информация должна в полном объеме'
                     ' предоставлять данные исполнителю.\n'
                     'Сейчас укажите полный адрес места выполнения заказа.',
                parse_mode='HTML',
            )

    except Exception as e:
        logger.error(f'Error in after_help_phone -> {e}')
