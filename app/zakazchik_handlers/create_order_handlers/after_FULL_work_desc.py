from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger

after_full_work_desc_router = Router()


@after_full_work_desc_router.message(CreateOrderStates.FULL_work_desc)
async def after_full_work_desc_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(FULL_work_desc=message.text)
        await state.set_state(CreateOrderStates.FULL_phones)

        await message.answer(
            text='<b>Создание нового заказа. Добавление подробной информации</b>\n\n'
                 'Указанное вами описание работы сохранено. Теперь укажите все контактные лица и их номера телефонов.'
                 'Данная информация может быть вами написана в свободной форме.',
            parse_mode='HTML',
        )

    except Exception as e:
        logger.error(f'Error in after_full_work_desc -> {e}')
