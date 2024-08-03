import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from loguru import logger

from google_sheets import Sheet

to_google_sheets_router = Router()


@to_google_sheets_router.callback_query(F.data.contains('to_google_sheets'))
async def to_google_sheets_handler(callback: CallbackQuery, state: FSMContext):
    try:
        load_dotenv()
        sprid = os.environ.get('SPREADSHEET_ID')
        await callback.answer()
        await state.clear()

        await Sheet().write_all_to_google_table()
        await callback.message.answer(
            text=f'Данные успешно выгружены в таблицу!\n'
                 f'<a href="https://docs.google.com/spreadsheets/d/{sprid}/edit"></a>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Назад',
                                      callback_data='admin_view_options_excel')],
            ])
        )

    except Exception as e:
        logger.error(f'Error in to_google_sheets -> {e}')
