import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import Chat
from app.generators import gpt_text
from app.database.requests import set_user, handle_anketa, get_anketa, save_chat_message

user = Router()

@user.callback_query(F.data == "back")
async def handle_back_button(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.answer(
        "Вы вернулись в главное меню",
        reply_markup=kb.main_inline
    )
    await callback_query.answer()

@user.callback_query(F.data == "chat")
async def start_chat_from_inline(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Chat.text)
    await callback_query.message.answer(
        "Введите ваш вопрос (для выхода нажмите 'Назад' или введите /Назад)",
        reply_markup=kb.back_button
    )
    await callback_query.answer()

@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await set_user(message.from_user.id)
    await message.answer(
        "Добро пожаловать! Это новый бот с ИИ",
        reply_markup=kb.main_inline
    )
    await state.clear()

@user.message(F.text == "Чат")
async def chatting(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer(
        "Введите ваш вопрос (для выхода нажмите 'Назад' или введите /Назад)",
        reply_markup=kb.back_button
    )

@user.message(Chat.text)
async def process_chat_message(message: Message, state: FSMContext):
    if message.text.lower() == "/назад":
        await state.clear()
        await message.answer("Вы вернулись в главное меню", reply_markup=kb.main_inline)
        return

    await state.set_state(Chat.wait)
    await message.answer("Ваш запрос обрабатывается...", reply_markup=kb.back_button)

    try:
        response = await gpt_text(message.text)
        await save_chat_message(message.from_user.id, message.text, response)
        await state.set_state(Chat.text)
        await message.answer(response, reply_markup=kb.back_button)
    except Exception as e:
        await state.set_state(Chat.text)
        await message.answer(f"Произошла ошибка: {e}", reply_markup=kb.back_button)

@user.message(Chat.wait)
async def wait_wait(message: Message, state: FSMContext):
    if message.text.lower() == "/назад":
        await state.clear()
        await message.answer("Вы вернулись в главное меню", reply_markup=kb.main_inline)
    else:
        await message.answer("Пожалуйста, подождите, пока обрабатывается предыдущий запрос.")

@user.message(F.text == 'Гороскоп')
async def get_horo(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer(
        'Введите дату и место рождения: город / дд.мм.гггг / точное время',
        reply_markup=kb.back_button
    )

@user.message(F.text == 'Анкета')
async def start_anketa(message: Message, state: FSMContext):
    await state.set_state(Chat.anketa)
    await message.answer('Заполни анкету. Начнем с имени. Как тебя зовут?')

@user.message(Chat.anketa)
async def process_anketa(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if 'name' not in user_data:
        await state.update_data(name=message.text)
        await message.answer('Отлично! Теперь укажи город рождения.')
        return
    if 'city_birth' not in user_data:
        await state.update_data(city_birth=message.text)
        await message.answer('Хорошо. Укажи дату рождения в формате дд.мм.гггг (например, 01.01.1990).')
        return
    if 'date_birth' not in user_data:
        await state.update_data(date_birth=message.text)
        await message.answer('Теперь укажи время рождения в формате чч:мм (например, 14:30).')
        return
    if 'time_birth' not in user_data:
        await state.update_data(time_birth=message.text)
        data = await state.get_data()
        await handle_anketa(
            tg_id=message.from_user.id,
            name=data['name'],
            city_birth=data['city_birth'],
            date_birth=data['date_birth'],
            time_birth=message.text
        )
        await message.answer('Анкета успешно заполнена! Спасибо!', reply_markup=kb.main_inline)
        await state.clear()