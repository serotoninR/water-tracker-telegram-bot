from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)

from db import DataBase
from setup_logging import logger

from .commands import cmd_calc, view_daily_norm
from .keyboards import reply_kb_add_amount
from .states import WaterLog

router = Router()


# Расчет нормы
@router.message(F.text == "🧪 Расчет нормы")
async def handle_calc_norm(message: Message, state: FSMContext):
    await cmd_calc(message, state)


# Вывод суточной нормы
@router.message(F.text == "💧 Показать суточную норму")
async def handle_view_norm(message: Message, db: DataBase):
    await view_daily_norm(message, db)


# Пополнение воды
@router.message(F.text == "🥤 Выпить воды")
async def handle_add_amount(message: Message, state: FSMContext):
    await state.clear()
    logger.info("Состояние очищено.")
    await state.set_state(WaterLog.waiting_for_amount)
    await message.answer(
        "🔢 Введите количество выпитой воды в мл (вручную - только цифры)",
        reply_markup=reply_kb_add_amount,
    )


# Вывод статистики
@router.message(F.text == "📊 Статистика")
async def handle_stats(message: Message, db: DataBase):
    user_id = message.from_user.id
    date = message.date.strftime("%Y-%m-%d")
    today_amount = await db.get_today_water(user_id, date)
    daily_norm = await db.view_daily_norm(user_id)
    if today_amount and daily_norm != 0:
        fill_percentages = (today_amount / daily_norm) * 10
        full_squares = "█" * int(fill_percentages)
        empty_squares = "░" * (10 - int(fill_percentages))
        scale = full_squares + empty_squares if empty_squares else ""
    else:
        scale = "Нет данных"
        fill_percentages = 0
    await message.answer(
        f"📊 Сегодня выпито {today_amount}/"
        f"{str(daily_norm) + ' мл' if daily_norm else 'Нет нормы'}\n\n"
        f"[{scale}] {int(fill_percentages * 10)}%"
    )
