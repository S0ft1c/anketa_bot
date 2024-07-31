from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_to_zakazhick_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',
                          callback_data='ya_zakazchik')]
])
