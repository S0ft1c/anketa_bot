from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger

after_full_address_router = Router()


@after_full_address_router.message(CreateOrderStates.FULL_address)
async def after_full_address_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(FULL_address=message.text)

        await state.set_state(CreateOrderStates.FULL_work_desc)

        await message.answer(
            text='<b>Создание нового заказа. Добавление подробной информации</b>\n\n'
                 'Указанный полный адрес сохранен! Теперь укажите полное описание работы в свободной форме.',
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(f'Erro in after_full_address_handler -> {e}')
