from aiogram.fsm.state import State, StatesGroup


# Состояние запроса веса в КГ для расчета суточной нормы
class Calculate(StatesGroup):
    waiting_for_weight = State()


# Ожидание вноса выпитой воды
class WaterLog(StatesGroup):
    waiting_for_amount = State()
