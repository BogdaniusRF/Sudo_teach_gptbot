from aiogram.fsm.state import StatesGroup, State

class Chat(StatesGroup):
    text = State()
    wait = State()
    anketa = State()  # New state for anketa form
    

# Для рассылок
class Newsletter(StatesGroup):   
    message = State()

