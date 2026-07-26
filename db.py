from sqlalchemy import Integer, String, func, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from setup_logging import logger

# Настройка движка (SQLAlchemy)
engine = create_async_engine("sqlite+aiosqlite:///tables.db")
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# Описание таблиц как классов
class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    daily_norm: Mapped[int] = mapped_column(Integer, default=0)


class WaterLog(Base):
    __tablename__ = "water_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer)
    date: Mapped[str] = mapped_column(String)


# Новый класс DataBase
class DataBase:
    # Инициализация БД
    async def init_db(self) -> None:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Таблицы базы данных успешно инициализированы.")
        except Exception as e:
            logger.error(f"Ошибка при инициализации базы данных: {e}")

    # Сохранение пользователя и/или добавление/обновление нормы
    async def save_user(self, user_id: int, daily_norm: int) -> None:
        try:
            async with async_session() as session:
                # "upsert" обновить или вставить
                async with session.begin():
                    user = await session.get(User, user_id)
                    if user:
                        user.daily_norm = daily_norm
                    else:
                        session.add(User(user_id=user_id, daily_norm=daily_norm))
            logger.info(
                f"Добавлен или обновлен пользователь {user_id} с суточной нормой: {daily_norm} мл"
            )
        except Exception as e:
            logger.error(f"Ошибка при сохранении пользователя {user_id}: {e}")

    # Увидеть суточную норму
    async def view_daily_norm(self, user_id: int) -> int | None:
        try:
            async with async_session() as session:
                user = await session.get(User, user_id)
                return user.daily_norm if user else None
        except Exception as e:
            logger.error(f"Ошибка при получении нормы для пользователя {user_id}: {e}")
            return None

    # Добавить запись выпивки воды
    async def add_water_log(self, user_id: int, amount: int, date: str) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    session.add(WaterLog(user_id=user_id, amount=amount, date=date))
            logger.info(
                f"Запись добавлена: {amount} мл для user_id {user_id} на дату {date}"
            )
        except Exception as e:
            logger.error(f"Ошибка при добавлении записи воды для {user_id}: {e}")

    # Количество выпитой воды за сутки
    async def get_today_water(self, user_id: int, date: str) -> int:
        try:
            async with async_session() as session:
                stmt = select(func.sum(WaterLog.amount)).where(
                    WaterLog.user_id == user_id, WaterLog.date == date
                )
                result = await session.execute(stmt)
                return result.scalar() or 0
        except Exception as e:
            logger.error(
                f"Ошибка при получении выпитой воды за сегодня для {user_id}: {e}"
            )
            return 0
