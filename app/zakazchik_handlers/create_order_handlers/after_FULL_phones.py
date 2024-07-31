from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from .back_to_zakazhick_btn import back_to_zakazhick_btn
from .create_order_states import CreateOrderStates

after_FULL_phones_router = Router()


@after_FULL_phones_router.message(CreateOrderStates.FULL_phones)
async def after_full_phones_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(FULL_phones=message.text)
        await state.set_state(CreateOrderStates.FULL_additional_info)

        await message.answer(
            text='<b>Контактные лица были сохранены в подробную информацию</b> '
                 '<i>ℹ️ Последний шаг! Укажите доп. информацию.</i>\n\n'
                 'Быть может есть какие-то моменты, которые нужны исполнителю для выполнения заказа качественно, но'
                 ' они не были еще указаны. Тут им самое место =)',
            parse_mode='HTML',
            reply_markup=back_to_zakazhick_btn,
        )

    except Exception as e:
        logger.error(f'Error in after_full_phones_handler -> {e}')
