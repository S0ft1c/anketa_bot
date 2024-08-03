from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from sqlite_database import DB


class AddAdmin(StatesGroup):
    user_id = State()


add_admin_to_admins_router = Router()


@add_admin_to_admins_router.callback_query(F.data.contains('add_admin_to_admins'))
async def add_admin_to_admins(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.clear()

        await state.set_state(AddAdmin.user_id)
        await callback.message.answer(
            text='Хорошо. Теперь введите id пользователя, которого вы хотите сделать администратором',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='open_admin_command')]
            ])
        )

    except Exception as e:
        logger.error(f'Error in add_admin_to_admins -> {e}')


@add_admin_to_admins_router.message(AddAdmin.user_id)
async def add_admin_to_admins_2(message: Message, state: FSMContext):
    try:
        if all(el.isdigit() for el in message.text):
            await state.clear()

            async with DB() as db:
                lastrowid = await db.insert_admin(telegram_id=message.text)

            await message.answer(
                text='Пользователь успешно сделан администратором',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Назад', callback_data='open_admin_command')]
                ])
            )
        else:
            await message.answer(
                text='Введенный вами id некорректен. Попробуйте еще раз.',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Назад', callback_data='open_admin_command')]
                ])
            )
    except Exception as e:
        logger.error(f'Error in add_admin_to_admins_2 -> {e}')
