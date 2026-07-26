from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from db import DataBase
from setup_logging import logger

from .keyboards import reply_kb_default
from .schemas import WaterAmountInput, WeightInput
from .states import Calculate, WaterLog

router = Router()


# Процедура расчета объема воды
@router.message(Calculate.waiting_for_weight)
async def process_weight(message: types.Message, state: FSMContext, db: DataBase):
    user_id = message.from_user.id
    weight_text = message.text.strip()

    # Проверка на отмену
    if weight_text == "❌ Отмена":
        await state.clear()
        await message.answer("⭕ Действие отменено", reply_markup=reply_kb_default)
        return

    try:
        data = WeightInput(weight=weight_text)
        weight = data.weight
    except ValidationError as e:
        error = e.errors()[0]
        await message.answer(f"❌ {error['msg']}\n\n🔄 Попробуйте еще раз")
        return

    # ✅ Всё ок, основная логика
    logger.info(f"Принят вес {weight} кг от пользователя.")
    await state.clear()

    daily_allowance = int((weight * 30) * 0.8)
    await db.save_user(user_id, daily_allowance)

    await message.answer(
        f"Ваша суточная норма потребления чистой воды:\n\n{daily_allowance} мл\n"
        "💧 Пейте воду и будьте здоровы!",
        reply_markup=reply_kb_default,
    )


# Внесение воды
@router.message(WaterLog.waiting_for_amount)
async def process_add_amount(message: types.Message, state: FSMContext, db: DataBase):
    user_id = message.from_user.id
    text = message.text
    date = message.date.strftime("%Y-%m-%d")

    if text == "❌ Отмена":
        await state.clear()
        await message.answer("⭕ Действие отменено", reply_markup=reply_kb_default)
        return

    text = message.text.lower().replace("мл", "").strip()
    date = message.date.strftime("%Y-%m-%d")

    try:
        data = WaterAmountInput(amount=text)
        amount = data.amount
    except ValidationError as e:
        error = e.errors()[0]
        await message.answer(f"❌ {error['msg']}\n\n🔄 Попробуйте еще раз")
        return

    await state.clear()
    await db.add_water_log(user_id, amount, date)
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
        f"✅ Принято {amount} мл, добавлена запись\n\n"
        f"📊 Сегодня выпито {today_amount}/{daily_norm} мл\n"
        f"[{scale}] {int(fill_percentages * 10)}%",
        reply_markup=reply_kb_default,
    )
