import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import Chat
from app.generators import gpt_text
# from app.generators import get_horoscope
from app.database.requests import set_user, handle_anketa, get_anketa



user = Router()



@user.message(F.text == 'Отмена')
@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await set_user(message.from_user.id)
    await message.answer('Добро пожаловать! Это новый бот с ИИ',reply_markup=kb.main)
    await state.clear

@user.message(F.text == 'Чат')
async def chatting(message:Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer('Введите ваш вопрос')

@user.message(F.text == 'Гороскоп')
async def get_horo(message:Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer('Введите вашу дату и место рождения: город / дд.мм.гггг / точное время')

@user.message(Chat.text)
async def chat_response(message:Message, state: FSMContext):
    await state.set_state(Chat.wait)
    response = await gpt_text(message.text)
    await message.answer(response)
    await state.clear()

@user.message(Chat.wait)
async def wait_wait(message:Message, state: FSMContext):
    await message.answer ('Ваше сообзение обрабатывается, подождите...')


# Новая функция для начала заполнения анкеты №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
@user.message(F.text == 'Анкета')
async def start_anketa(message: Message, state: FSMContext):
    await state.set_state(Chat.anketa)
    await message.answer('Заполни анкету. Начнем с имени. Как тебя зовут?')


# Обработка данных анкеты через состояние Chat.anketa
@user.message(Chat.anketa)
async def process_anketa(message: Message, state: FSMContext):
    # Получаем текущие данные из состояния
    user_data = await state.get_data()
    
    # Если данных еще нет, начинаем с имени
    if 'name' not in user_data:
        await state.update_data(name=message.text)
        await message.answer('Отлично! Теперь укажи город рождения.')
        return
    
    # Если имя есть, но нет города
    if 'city_birth' not in user_data:
        await state.update_data(city_birth=message.text)
        await message.answer('Хорошо. Укажи дату рождения в формате дд.мм.гггг (например, 01.01.1990).')
        return
    
    # Если город есть, но нет даты
    if 'date_birth' not in user_data:
        await state.update_data(date_birth=message.text)
        await message.answer('Теперь укажи время рождения в формате чч:мм (например, 14:30).')
        return
    
    # Если все данные кроме времени собраны, сохраняем время и завершаем
    if 'time_birth' not in user_data:
        await state.update_data(time_birth=message.text)
        
        # Получаем все данные из состояния
        data = await state.get_data()
        
        # Сохраняем в базу через handle_anketa
        await handle_anketa(
            tg_id=message.from_user.id,
            name=data['name'],
            city_birth=data['city_birth'],
            date_birth=data['date_birth'],
            time_birth=message.text
        )
        
        await message.answer('Анкета успешно заполнена! Спасибо!')
        await state.clear()  # Очищаем состояние после завершения


# Опционально: проверка данных анкеты
# @user.message(F.text == 'Моя анкета')
# async def show_anketa(message: Message, state: FSMContext):
#     anketa = await get_anketa(message.from_user.id)
#     if anketa:
#         response = (
#             f"Ваша анкета:\n"
#             f"Имя: {anketa.name}\n"
#             f"Город рождения: {anketa.city_birth}\n"
#             f"Дата рождения: {anketa.date_birth}\n"
#             f"Время рождения: {anketa.time_birth}"
#         )
#     else:
#         response = "Вы еще не заполнили анкету. Нажмите 'Анкета', чтобы начать."
#     await message.answer(response)

