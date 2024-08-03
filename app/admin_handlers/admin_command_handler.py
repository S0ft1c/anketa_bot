import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv
from loguru import logger

from sqlite_database import DB


async def create_admin_ids():
    load_dotenv()
    admin_ids = set(int(el) for el in os.environ.get('ADMIN_IDS').split(','))
    async with DB() as db:
        admins_from_db = await db.select_all_admins()
        admins_ids_from_db = [el['telegram_id'] for el in admins_from_db]
        admin_ids = admin_ids | set(admins_ids_from_db)
    return admin_ids


admin_command_router = Router()


@admin_command_router.message(
    (F.text == '/admin')
)
async def admin_command_handler(message: Message, state: FSMContext):
    try:
        if message.from_user.id not in await create_admin_ids():
            return

        await state.clear()
        await message.answer(
            text=f'<b>Вы вошли в админ. панель!</b>\n'
                 f'Выберите действие',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Подтверждение часов', callback_data='admin_hours_commit_list')],
                [InlineKeyboardButton(text='Долгосрочные проекты', callback_data='admin_long_projects_list')],
                [InlineKeyboardButton(text='Выгрузить отчеты', callback_data='admin_view_options_excel')],
                [InlineKeyboardButton(text='Добавить администратора', callback_data='add_admin_to_admins')]
            ])
        )
    except Exception as e:
        logger.error(f'Error in admin_command_handler: {e}')


@admin_command_router.callback_query(
    (F.data.contains('open_admin_command'))
)
async def admin_command_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        if callback.from_user.id not in await create_admin_ids():
            return

        await state.clear()
        await callback.message.answer(
            text=f'<b>Вы вошли в админ. панель!</b>\n'
                 f'Выберите действие',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Подтверждение часов', callback_data='admin_hours_commit_list')],
                [InlineKeyboardButton(text='Долгосрочные проекты', callback_data='admin_long_projects_list')],
                [InlineKeyboardButton(text='Выгрузить отчеты', callback_data='admin_view_options_excel')],
                [InlineKeyboardButton(text='Добавить администратора', callback_data='add_admin_to_admins')]
            ])
        )
    except Exception as e:
        logger.error(f'Error in admin_command_handler: {e}')
