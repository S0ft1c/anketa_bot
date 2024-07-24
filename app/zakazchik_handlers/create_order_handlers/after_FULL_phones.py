from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger

after_FULL_phones_router = Router()


@after_FULL_phones_router.message(CreateOrderStates.FULL_phones)
async def after_full_phones_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(FULL_phones=message.text)
        await state.set_state(CreateOrderStates.FULL_additional_info)

        await message.answer(
            text='<b>Создание нового заказа. Добавление подробной информации</b>\n\n'
                 'Прекрасно! Последний шаг - укажите какую-либо дополнительную информацию, '
                 'что должен знать исполнитель.',
            parse_mode='HTML'
        )

    except Exception as e:
        logger.error(f'Error in after_full_phones_handler -> {e}')
