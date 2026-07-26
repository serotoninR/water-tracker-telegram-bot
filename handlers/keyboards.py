from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Клавиатура старта
reply_kb_default = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧪 Расчет нормы"),
            KeyboardButton(text="💧 Показать суточную норму"),
        ],
        [KeyboardButton(text="🥤 Выпить воды"), KeyboardButton(text="📊 Статистика")],
    ],
    resize_keyboard=True,
)

# Клавиатура добавки воды
reply_kb_add_amount = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="100 мл"), KeyboardButton(text="250 мл")],
        [KeyboardButton(text="❌ Отмена")],
    ],
    resize_keyboard=True,
)

# Кнопка отмены
reply_kb_cancel = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]], resize_keyboard=True
)
