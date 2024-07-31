from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

pure_start_router = Router()


@pure_start_router.message(CommandStart(deep_link=False))
async def pure_start(message: Message):
    try:
        await message.answer(
            text='<i>Привет!</i> В нашем боте вы можете как выполнять заказы, так и создавать собственные.\n'
                 'Для начала выберите кто вы сегодня =)',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='💼 Я заказчик', callback_data='ya_zakazchik'),
                 InlineKeyboardButton(text='👷‍♂️ Я исполнитель', callback_data='ya_ispolnitel')],
            ])
        )
    except Exception as e:
        logger.error(f'Error in pure_start handler! -> {e}')
