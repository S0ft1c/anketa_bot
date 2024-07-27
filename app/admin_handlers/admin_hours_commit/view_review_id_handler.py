from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB

view_review_id_router = Router()


async def create_kb(review_id, counted_hours):
    if counted_hours == 'Не удалось рассчитать.':
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Указать свое количество часов',
                                  callback_data=f'admin_self_hours_commit={review_id}'), ],
            [InlineKeyboardButton(text='Исполнитель не пришел',
                                  callback_data=f'admin_minus_worker={review_id}'), ],
            [InlineKeyboardButton(text='Назад',
                                  callback_data='admin_hours_commit_list')],
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить количество часов',
                                  callback_data=f'admin_submit_hours_commit={review_id}={counted_hours}'), ],
            [InlineKeyboardButton(text='Указать свое количество часов',
                                  callback_data=f'admin_self_hours_commit={review_id}'), ],
            [InlineKeyboardButton(text='Исполнитель не пришел',
                                  callback_data=f'admin_minus_worker={review_id}'), ],
            [InlineKeyboardButton(text='Назад',
                                  callback_data='admin_hours_commit_list')],
        ])


@view_review_id_router.callback_query(F.data.contains('view_review_id'))
async def view_review_id_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')
        review_id = callback.data.split('=')[-1]

        async with DB() as db:
            rev_info = await db.select_review_by_id(review_id)

        await callback.message.answer(
            text='<b><i>Информация по заказу:</i></b>\n\n'
                 f'📅 <b>Заказ от {rev_info['date']}</b>\n'
                 f'👥 <i>Людей надо</i>:\n{rev_info['how_many_ppl']}\n'
                 f'🏠 <i>Адрес</i>:\n{rev_info['address']}\n'
                 f'🔧 <i>Описание работы</i>\n{rev_info['work_desc']}\n'
                 f'💵 <i>Оплата (руб/час)</i>\n{rev_info['payment']}\n'
                 f'📞 <i>Телефон для справок</i>\n{rev_info['help_phone']}\n\n'
                 f'ℹ️ <b>Подробная информация</b>\n'
                 f'🏠 <i>Адрес</i>:\n{rev_info['FULL_address']}\n'
                 f'🔧 <i>Описание работы</i>:\n{rev_info['FULL_work_desc']}\n'
                 f'📞 <i>Контактные лица</i>:\n{rev_info['FULL_phones']}\n'
                 f'📝<i>Доп. информация</i>:\n{rev_info['FULL_additional_info']}\n\n'
                 f'{f'<u>Это долгосрочный заказ. => Сроки {rev_info['long_days']} дн.</u>' if rev_info['long_time']
                 else f'Это не долгосрочный заказ.'}',
            parse_mode='HTML',
        )
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=f'<b>Отчет заказчика:</b>\n'
                 f'{rev_info["report"]}\n',
            parse_mode='HTML',
        )
        if rev_info['start_date'] and rev_info['end_date']:
            counted_hours = datetime.strptime(str(rev_info['end_date']), "%H:%M %d.%m.%Y") - \
                            datetime.strptime(str(rev_info['start_date']), "%H:%M %d.%m.%Y")
            counted_hours = int(counted_hours.total_seconds() // 3600)
        else:
            counted_hours = 'Не удалось рассчитать.'
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=f'<b>Время начала и конца, внесенное исполнителем:</b>\n'
                 f'{rev_info["start_date"]} -- {rev_info['end_date']}\n'
                 f'Посчитанное системой количество часов = {counted_hours}\n',
            parse_mode='HTML',
            reply_markup=await create_kb(review_id, counted_hours)
        )
    except Exception as e:
        logger.error(f'Error in view_review_id_handler: {e}')
