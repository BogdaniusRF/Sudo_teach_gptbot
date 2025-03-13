from app.database.models import async_session
from app.database.models import User, UserHoroAnketa
from sqlalchemy import select, update, delete, desc
from app.states import Newsletter


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner    



@connection
async def set_user(session,tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id))
        await session.commit()

@connection
async def get_user(session,tg_id):
    return await session.scalar(select(User).where(User.tg_id == tg_id))   

@connection
async def get_users(session):
    return await session.scalars(select(User))


# ниже должна быть функция "handle_anketa" для добавления данных в БД db.sqlite3 в таблицу "user_horo_anketa" спараметрами: session, tg_id, name, city_birth, date_birth, time_birth
@connection
async def handle_anketa(session, tg_id, name, city_birth, date_birth, time_birth):
    # Проверяем, существует ли запись с таким tg_id
    anketa = await session.scalar(select(UserHoroAnketa).where(UserHoroAnketa.tg_id == tg_id))
    
    if not anketa:
        # Если записи нет, создаем новую
        session.add(UserHoroAnketa(
            tg_id=tg_id,
            name=name,
            city_birth=city_birth,
            date_birth=date_birth,
            time_birth=time_birth
        ))
        await session.commit()
    else:
        # Если запись есть, обновляем существующие данные
        anketa.name = name
        anketa.city_birth = city_birth
        anketa.date_birth = date_birth
        anketa.time_birth = time_birth
        await session.commit()


# Опционально: функция для получения данных анкеты по tg_id
@connection
async def get_anketa(session, tg_id):
    return await session.scalar(select(UserHoroAnketa).where(UserHoroAnketa.tg_id == tg_id))