from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# main = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Чат')],
#     [KeyboardButton(text='Гороскоп')],
#     [KeyboardButton(text='Анкета')]
# ],
#                         resize_keyboard=True,
#                         input_field_placeholder='Выберете пункт меню')

# cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]],
#                             resize_keyboard=True)

# back_button = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='/Назад', callback_data='back_to_main')]
# ])

main_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Чат", callback_data="chat")],
    [InlineKeyboardButton(text='Гороскоп', callback_data='horoscope')],
    [InlineKeyboardButton(text='Анкета', callback_data='anketa')]
])

# Кнопка "Назад" (inline)
back_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")]
])