from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db import DataBase
from setup_logging import logger

from .keyboards import reply_kb_cancel, reply_kb_default
from .states import Calculate

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🔋 Приветствую, я бот для контроля потребления воды\n\n"
        "⬇️ Бот управляется кнопками снизу",
        reply_markup=reply_kb_default,
    )


@router.message(Command("calculation"))
async def cmd_calc(message: types.Message, state: FSMContext):
    await state.clear()
    logger.info("Состояние расчета очищено.")
    await state.set_state(Calculate.waiting_for_weight)
    await message.answer(
        "🔢 Напишите вес в КГ (только цифры)", reply_markup=reply_kb_cancel
    )


@router.message(Command("view_norm"))
async def view_daily_norm(message: types.Message, db: DataBase):
    user_id = message.from_user.id
    daily_norm = await db.view_daily_norm(user_id)
    await message.answer(
        f"♻️ Ваша суточная норма чистой воды:\n"
        f"{str(daily_norm) + ' мл' if daily_norm else 'Не установлена'}\n\n"
    )
