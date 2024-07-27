import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from loguru import logger

admin_command_router = Router()

load_dotenv()
admin_ids = set(int(el) for el in os.environ.get('ADMIN_IDS').split(','))
print(admin_ids)


@admin_command_router.message(Command('admin'), F.from_user.id.in_(admin_ids))
async def admin_command_handler(message: Message, state: FSMContext):
    try:
        await state.clear()
        await message.answer(
            text=f'<b>Вы вошли в админ. панель!</b>\n'
                 f'Выберите действие',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Подтверждение часов', callback_data='admin_hours_commit_list')],
            ])
        )
    except Exception as e:
        logger.error(f'Error in admin_command_handler: {e}')
