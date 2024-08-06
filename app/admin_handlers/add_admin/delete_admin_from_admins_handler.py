from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from loguru import logger

from sqlite_database import DB

delete_admin_from_admins_router = Router()


async def create_kb():
    async with DB() as db:
        admins = await db.select_all_admins()
    builder = InlineKeyboardBuilder()
    for admin in admins:
        builder.add(InlineKeyboardButton(text=str(admin['telegram_id']),
                                         callback_data=f'delete_admin_request={admin["telegram_id"]}'))
    return builder.adjust(1).as_markup()


@delete_admin_from_admins_router.callback_query(F.data.contains('delete_admin_from_admins'))
async def delete_admin_from_admins_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()

        async with DB() as db:
            admins = await db.select_all_admins()

        await callback.message.answer(
            text='Внизу указаны все id пользователей, которые обладают правами администратора.\n' +
                 'Просто нажмите на id пользователя, чтобы лишить его прав администратора.\n' +
                 'Вот все пользователи (это ссылки, просто перейдите и посмотрите кто это, чтобы потом удалить):\n' +
                 '\n'.join(
                     f'<a href="tg://user?id={admin['telegram_id']}">{admin['telegram_id']}</a>' for admin in admins
                 ),
            parse_mode=ParseMode.HTML,
            reply_markup=await create_kb()
        )

    except Exception as e:
        logger.error(f'Error while handling delete admin from admins handler: {e}')


@delete_admin_from_admins_router.callback_query(F.data.contains('delete_admin_request'))
async def delete_admin_from_admins_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()
        tg_id = callback.data.split('=')[-1]

        async with DB() as db:
            await db.delete_admin_by_telegram_id(tg_id)

        await callback.message.answer(
            text=f'Пользователь с id -> {tg_id} лишен прав администратора!',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='open_admin_command')],
            ])
        )

    except Exception as e:
        logger.error(f'Error in delete admin from admins handler: {e}')
