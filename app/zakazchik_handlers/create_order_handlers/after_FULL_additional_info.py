from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger

after_full_additional_info_router = Router()


@after_full_additional_info_router.message(CreateOrderStates.FULL_additional_info)
async def after_full_additional_info_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(FULL_additional_info=message.text)
        await state.set_state(CreateOrderStates.long_time)
        await message.answer(
            text='<b>Создание заказа. Указание долгосрочный ли заказ.</b>\n\n'
                 'Почти все. Теперь укажите является ли заказ долгосрочным.',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Да. Мой заказ долгосрочный', callback_data='yes_long_time'),
                 InlineKeyboardButton(text='Нет. Мой заказ не долгосрочный', callback_data='no_long_time')]
            ])
        )

    except Exception as e:
        logger.error(f'Error in after_full_additional_info_handler -> {e}')
