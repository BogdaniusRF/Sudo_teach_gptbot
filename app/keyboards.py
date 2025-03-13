from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
#import app.builder as builder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Чат')],
    [KeyboardButton(text='Гороскоп')],
    [KeyboardButton(text='Анкета')]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберете пункт меню')



cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]],
                            resize_keyboard=True)
