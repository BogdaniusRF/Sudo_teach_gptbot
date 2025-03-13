#from email import message
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, MessageId, message_id
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from app.states import Newsletter
from app.database.requests import get_users


admin = Router()

class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [127605342,7701995830,456]  # Список администраторов


# Далее будут хэндлеры для рассылки. Для этого нужно создать несколько состояний (States.py)
@admin.message(Admin(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)   # Бот ловит состояние 
    await message.answer('Введите сообщение для массовой рассылки')



@admin.message(Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    
    await message.answer('Рассылка началась')
    users = await get_users()
    for user in users:
        try:
            await message.send_copy(chat_id=user.tg_id)
            
        except Exception as e:
            print(e)
    await message.answer('Рассылка завершена')
    await state.clear()
    
