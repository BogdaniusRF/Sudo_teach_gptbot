from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column, declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

#from config import DB_URL

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3',
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class UserHoroAnketa(Base):
    __tablename__ = 'user_horo_anketa'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name = mapped_column(String)
    city_birth = mapped_column(String)
    date_birth = mapped_column(String)
    time_birth = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
