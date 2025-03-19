########################    ########################    ########################    ########################    
# Данный раздел - для работой с БД. Здесь производится подключеие к БД, запросы данных о пользвателях, внесение информации в БД.
# https://sudoteach.com/content/2/97
#
#
########################    ########################    ########################    ########################    




# Postgres
from app.database.models_Postgre import async_session
from app.database.models_Postgre import User, UserHoroAnketa
#SQlite3
# from app.database.models import async_session
# from app.database.models import User, UserHoroAnketa

from sqlalchemy import select, update, delete, desc
from app.states import Newsletter
from app.generators import gpt_embed
from app.database.models_Postgre import async_session, User, UserHoroAnketa, ChatHistory
from sqlalchemy import select
from app.generators import gpt_embed  # Добавляем импорт

def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner    

@connection
async def set_user(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        session.add(User(tg_id=tg_id))
        await session.commit()

@connection
async def get_user(session, tg_id):
    return await session.scalar(select(User).where(User.tg_id == tg_id))   

@connection
async def get_users(session):
    return await session.scalars(select(User))

@connection
async def handle_anketa(session, tg_id, name, city_birth, date_birth, time_birth):
    anketa = await session.scalar(select(UserHoroAnketa).where(UserHoroAnketa.tg_id == tg_id))
    if not anketa:
        session.add(UserHoroAnketa(
            tg_id=tg_id,
            name=name,
            city_birth=city_birth,
            date_birth=date_birth,
            time_birth=time_birth
        ))
    else:
        anketa.name = name
        anketa.city_birth = city_birth
        anketa.date_birth = date_birth
        anketa.time_birth = time_birth
    await session.commit()

@connection
async def get_anketa(session, tg_id):
    return await session.scalar(select(UserHoroAnketa).where(UserHoroAnketa.tg_id == tg_id))

@connection
async def save_chat_message(session, tg_id, question, response):
    question_vec = await gpt_embed(question)
    response_vec = await gpt_embed(response)
    session.add(ChatHistory(
        tg_id=tg_id,
        question=question,
        response=response,
        question_vector=question_vec,
        response_vector=response_vec
    ))
    await session.commit()