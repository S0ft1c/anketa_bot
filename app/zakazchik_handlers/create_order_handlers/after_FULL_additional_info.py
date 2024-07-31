from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from .create_order_states import CreateOrderStates

after_full_additional_info_router = Router()


@after_full_additional_info_router.message(CreateOrderStates.FULL_additional_info)
async def after_full_additional_info_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(FULL_additional_info=message.text)
        await state.set_state(CreateOrderStates.long_time)
        await message.answer(
            text='<b>Доп. информация сохранена!</b> '
                 '<i>Почти все. Осталось лишь указать является ли ваш заказ долгосрочным.</i>\n\n'
                 'Долгосрочный заказ это особенный заказ. Он выполняется не один день. '
                 'Если вам подходит такая опция, смело выбирайте <i>Да</i>.',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Да. Мой заказ долгосрочный', callback_data='yes_long_time'),
                 InlineKeyboardButton(text='Нет. Мой заказ не долгосрочный', callback_data='no_long_time')]
            ])
        )

    except Exception as e:
        logger.error(f'Error in after_full_additional_info_handler -> {e}')
